import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
    CheckCircle, Clock, AlertTriangle, Trash2, Plus,
    ListChecks, Users, Calendar, ChevronDown, ChevronUp,
    Wrench, Layers, UserCheck
} from 'lucide-react';

const API = '/api';

const priorityConfig = {
    High: { color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', icon: <AlertTriangle className="w-4 h-4" /> },
    Medium: { color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', icon: <Clock className="w-4 h-4" /> },
    Low: { color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/30', icon: <Layers className="w-4 h-4" /> },
};

export default function Tasks() {
    const [tasks, setTasks] = useState([]);
    const [staff, setStaff] = useState([]);
    const [attendance, setAttendance] = useState([]);
    const [tab, setTab] = useState('tasks');   // 'tasks' | 'staff' | 'attendance'
    const [showAddTask, setShowAddTask] = useState(false);
    const [showAddStaff, setShowAddStaff] = useState(false);
    const [loading, setLoading] = useState(true);
    const [today] = useState(new Date().toISOString().split('T')[0]);

    // New task form state
    const [newTask, setNewTask] = useState({ title: '', priority: 'Medium', service_queue: '' });
    // New staff form state
    const [newStaff, setNewStaff] = useState({ name: '', role: 'Guard', phone: '', salary: '', joined_at: '' });

    const fetchTasks = async () => {
        try { const r = await axios.get(`${API}/tasks`); setTasks(r.data); }
        catch (e) { console.error(e); }
    };
    const fetchStaff = async () => {
        try { const r = await axios.get(`${API}/staff`); setStaff(r.data); }
        catch (e) { console.error(e); }
    };
    const fetchAttendance = async () => {
        try { const r = await axios.get(`${API}/staff/attendance?date=${today}`); setAttendance(r.data); }
        catch (e) { console.error(e); }
    };

    useEffect(() => {
        const load = async () => {
            setLoading(true);
            await Promise.all([fetchTasks(), fetchStaff(), fetchAttendance()]);
            setLoading(false);
        };
        load();
    }, []);

    // ── Task actions ──
    const toggleTask = async (task) => {
        const newStatus = task.status === 'Completed' ? 'Pending' : 'Completed';
        await axios.put(`${API}/tasks/${task.id}`, { status: newStatus });
        fetchTasks();
    };
    const deleteTask = async (id) => {
        if (!window.confirm('Delete this task?')) return;
        await axios.delete(`${API}/tasks/${id}`);
        fetchTasks();
    };
    const addTask = async () => {
        if (!newTask.title.trim()) return;
        
        // If it's High priority or contains maintenance keywords, also create a Maintenance Request
        // so it shows up in the Issue Inbox
        const isMaintenance = newTask.priority === 'High' || 
                             newTask.title.toLowerCase().includes('repair') || 
                             newTask.title.toLowerCase().includes('broken') ||
                             newTask.title.toLowerCase().includes('leak');

        if (isMaintenance) {
            await axios.post(`${API}/maintenance`, {
                description: newTask.title,
                priority: newTask.priority === 'High' ? 'Critical' : 'Routine',
                status: 'Pending'
            });
        }

        await axios.post(`${API}/tasks`, newTask);
        setNewTask({ title: '', priority: 'Medium', service_queue: '' });
        setShowAddTask(false);
        fetchTasks();
    };

    // ── Staff actions ──
    const addStaff = async () => {
        if (!newStaff.name.trim()) return;
        await axios.post(`${API}/staff`, newStaff);
        setNewStaff({ name: '', role: 'Guard', phone: '', salary: '', joined_at: '' });
        setShowAddStaff(false);
        fetchStaff();
        fetchAttendance();
    };
    const removeStaff = async (id) => {
        if (!window.confirm('Remove this staff member?')) return;
        await axios.delete(`${API}/staff/${id}`);
        fetchStaff();
        fetchAttendance();
    };

    // ── Attendance actions ──
    const markAttendance = async (staffId, status, timeIn = null, timeOut = null) => {
        await axios.post(`${API}/staff/attendance`, {
            staff_id: staffId, date: today, status, time_in: timeIn, time_out: timeOut
        });
        fetchAttendance();
    };

    const pendingCount = tasks.filter(t => t.status === 'Pending').length;
    const urgentCount = tasks.filter(t => t.priority === 'High' && t.status === 'Pending').length;

    if (loading) return (
        <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
        </div>
    );

    return (
        <div className="p-6 space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white">Task & Staff Control</h1>
                    <p className="text-white/50 text-sm mt-1">Manage daily operations, staff, and micro-tasks</p>
                </div>
                <div className="flex gap-3">
                    {urgentCount > 0 && (
                        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-red-500/15 border border-red-500/30 text-red-400 text-sm font-medium">
                            <AlertTriangle className="w-4 h-4" />
                            {urgentCount} Urgent
                        </div>
                    )}
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 text-sm font-medium">
                        <Clock className="w-4 h-4" />
                        {pendingCount} Pending
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 p-1 rounded-2xl bg-white/5 border border-white/10 w-fit">
                {[
                    { key: 'tasks', label: 'Tasks', icon: <ListChecks className="w-4 h-4" /> },
                    { key: 'staff', label: 'Staff', icon: <Users className="w-4 h-4" /> },
                    { key: 'attendance', label: 'Attendance', icon: <UserCheck className="w-4 h-4" /> },
                ].map(t => (
                    <button
                        key={t.key}
                        onClick={() => setTab(t.key)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${tab === t.key
                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
                            : 'text-white/50 hover:text-white hover:bg-white/5'
                            }`}
                    >
                        {t.icon} {t.label}
                    </button>
                ))}
            </div>

            {/* ──────────── TASKS TAB ──────────── */}
            {tab === 'tasks' && (
                <div className="space-y-4">
                    <div className="flex justify-end">
                        <button onClick={() => setShowAddTask(!showAddTask)}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/80 hover:bg-blue-600 text-white text-sm font-medium transition-all">
                            <Plus className="w-4 h-4" /> New Task
                        </button>
                    </div>

                    {/* Add Task Form */}
                    <AnimatePresence>
                        {showAddTask && (
                            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
                                className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl space-y-4">
                                <h3 className="text-white font-semibold">Create New Task</h3>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <input value={newTask.title} onChange={e => setNewTask({ ...newTask, title: e.target.value })}
                                        placeholder="Task description..." type="text"
                                        className="col-span-1 md:col-span-2 px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-blue-500/50" />
                                    <select value={newTask.priority} onChange={e => setNewTask({ ...newTask, priority: e.target.value })}
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white focus:outline-none focus:border-blue-500/50">
                                        <option value="High">🔴 High (Urgent)</option>
                                        <option value="Medium">🟡 Medium (Routine)</option>
                                        <option value="Low">🔵 Low (Service Queue)</option>
                                    </select>
                                </div>
                                <input value={newTask.service_queue} onChange={e => setNewTask({ ...newTask, service_queue: e.target.value })}
                                    placeholder="Service Queue (e.g. Carpenter, Plumber) — leave blank if not needed"
                                    type="text"
                                    className="w-full px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-blue-500/50" />
                                <div className="flex gap-3">
                                    <button onClick={addTask}
                                        className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-all">
                                        Add Task
                                    </button>
                                    <button onClick={() => setShowAddTask(false)}
                                        className="px-5 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-white/60 text-sm transition-all">
                                        Cancel
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Task List */}
                    {['High', 'Medium', 'Low'].map(priority => {
                        const groupTasks = tasks.filter(t => t.priority === priority);
                        if (!groupTasks.length) return null;
                        const cfg = priorityConfig[priority];
                        return (
                            <div key={priority} className="space-y-2">
                                <div className={`flex items-center gap-2 text-xs font-bold uppercase tracking-wider ${cfg.color} mb-2`}>
                                    {cfg.icon}
                                    {priority === 'High' ? 'Urgent Tasks' : priority === 'Medium' ? 'Daily Routine' : 'Service Queue'}
                                    <span className="ml-auto opacity-60">{groupTasks.length} tasks</span>
                                </div>
                                {groupTasks.map(task => (
                                    <motion.div key={task.id} layout initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                        className={`flex items-center gap-4 p-4 rounded-2xl border backdrop-blur-xl transition-all ${task.status === 'Completed'
                                            ? 'bg-white/3 border-white/5 opacity-60'
                                            : `${cfg.bg} ${cfg.border}`
                                            }`}>
                                        <button onClick={() => toggleTask(task)}
                                            className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${task.status === 'Completed'
                                                ? 'bg-green-500 border-green-500'
                                                : 'border-white/30 hover:border-green-400'
                                                }`}>
                                            {task.status === 'Completed' && <CheckCircle className="w-4 h-4 text-white" />}
                                        </button>
                                        <div className="flex-1 min-w-0">
                                            <p className={`text-sm font-medium ${task.status === 'Completed' ? 'line-through text-white/40' : 'text-white'}`}>
                                                {task.title}
                                            </p>
                                            {task.service_queue && (
                                                <span className="text-xs text-blue-400 mt-0.5 inline-flex items-center gap-1">
                                                    <Wrench className="w-3 h-3" /> {task.service_queue} Queue
                                                </span>
                                            )}
                                        </div>
                                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${task.status === 'Completed' ? 'bg-green-500/20 text-green-400' : 'bg-white/10 text-white/50'
                                            }`}>{task.status}</span>
                                        <button onClick={() => deleteTask(task.id)}
                                            className="text-red-400/60 hover:text-red-400 transition-colors ml-2">
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </motion.div>
                                ))}
                            </div>
                        );
                    })}

                    {tasks.length === 0 && (
                        <div className="text-center py-12 text-white/30">
                            <ListChecks className="w-12 h-12 mx-auto mb-3 opacity-30" />
                            <p>No tasks yet. Add a task to get started.</p>
                        </div>
                    )}
                </div>
            )}

            {/* ──────────── STAFF TAB ──────────── */}
            {tab === 'staff' && (
                <div className="space-y-4">
                    <div className="flex justify-end">
                        <button onClick={() => setShowAddStaff(!showAddStaff)}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/80 hover:bg-blue-600 text-white text-sm font-medium transition-all">
                            <Plus className="w-4 h-4" /> Add Staff
                        </button>
                    </div>

                    <AnimatePresence>
                        {showAddStaff && (
                            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
                                className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl space-y-4">
                                <h3 className="text-white font-semibold">Add Staff Member</h3>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <input value={newStaff.name} onChange={e => setNewStaff({ ...newStaff, name: e.target.value })}
                                        placeholder="Full Name" type="text"
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-blue-500/50" />
                                    <select value={newStaff.role} onChange={e => setNewStaff({ ...newStaff, role: e.target.value })}
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white focus:outline-none focus:border-blue-500/50">
                                        <option value="Guard">Guard</option>
                                        <option value="Cleaner">Cleaner</option>
                                        <option value="Other">Other</option>
                                    </select>
                                    <input value={newStaff.phone} onChange={e => setNewStaff({ ...newStaff, phone: e.target.value })}
                                        placeholder="Phone Number" type="text"
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-blue-500/50" />
                                    <input value={newStaff.salary} onChange={e => setNewStaff({ ...newStaff, salary: e.target.value })}
                                        placeholder="Monthly Salary (Rs.)" type="number"
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-blue-500/50" />
                                    <input value={newStaff.joined_at} onChange={e => setNewStaff({ ...newStaff, joined_at: e.target.value })}
                                        type="date"
                                        className="px-4 py-2.5 rounded-xl bg-black/20 border border-white/10 text-white focus:outline-none focus:border-blue-500/50" />
                                </div>
                                <div className="flex gap-3">
                                    <button onClick={addStaff}
                                        className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-all">Add Staff</button>
                                    <button onClick={() => setShowAddStaff(false)}
                                        className="px-5 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-white/60 text-sm transition-all">Cancel</button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {staff.map(s => (
                            <div key={s.id} className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <p className="text-white font-semibold">{s.name}</p>
                                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block ${s.role === 'Guard' ? 'bg-blue-500/20 text-blue-400' : 'bg-green-500/20 text-green-400'
                                            }`}>{s.role}</span>
                                    </div>
                                    <button onClick={() => removeStaff(s.id)} className="text-red-400/60 hover:text-red-400 transition-colors">
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                                <div className="mt-3 text-sm text-white/50 space-y-1">
                                    {s.phone && <p>📞 {s.phone}</p>}
                                    {s.salary && <p>💰 Rs. {s.salary.toLocaleString()}/month</p>}
                                    {s.joined_at && <p>📅 Joined: {s.joined_at}</p>}
                                </div>
                            </div>
                        ))}
                        {staff.length === 0 && (
                            <div className="col-span-full text-center py-12 text-white/30">
                                <Users className="w-12 h-12 mx-auto mb-3 opacity-30" />
                                <p>No staff members added yet.</p>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* ──────────── ATTENDANCE TAB ──────────── */}
            {tab === 'attendance' && (
                <div className="space-y-4">
                    <div className="flex items-center gap-3 p-4 rounded-2xl bg-blue-500/10 border border-blue-500/20">
                        <Calendar className="w-5 h-5 text-blue-400" />
                        <p className="text-blue-300 font-medium text-sm">Today's Attendance — {today}</p>
                    </div>

                    {attendance.length === 0 ? (
                        <div className="text-center py-12 text-white/30">
                            <UserCheck className="w-12 h-12 mx-auto mb-3 opacity-30" />
                            <p>Add staff members first to track attendance.</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {attendance.map(a => (
                                <div key={a.staff_id} className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl">
                                    <div className="flex items-center justify-between flex-wrap gap-3">
                                        <div>
                                            <p className="text-white font-semibold">{a.name}</p>
                                            <span className="text-xs text-white/40">{a.role}</span>
                                        </div>
                                        <div className="flex gap-2">
                                            {['Present', 'Absent', 'Late'].map(s => (
                                                <button key={s} onClick={() => markAttendance(a.staff_id, s)}
                                                    className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${a.status === s
                                                        ? s === 'Present' ? 'bg-green-500 text-white'
                                                            : s === 'Absent' ? 'bg-red-500 text-white'
                                                                : 'bg-yellow-500 text-white'
                                                        : 'bg-white/5 text-white/50 hover:bg-white/10'
                                                        }`}>{s}</button>
                                            ))}
                                        </div>
                                    </div>
                                    {a.status === 'Present' || a.status === 'Late' ? (
                                        <div className="grid grid-cols-2 gap-3 mt-3">
                                            <div>
                                                <label className="text-xs text-white/40 uppercase tracking-wider">Time In</label>
                                                <input type="time" defaultValue={a.time_in || ''}
                                                    onBlur={e => markAttendance(a.staff_id, a.status, e.target.value, a.time_out)}
                                                    className="w-full mt-1 px-3 py-2 rounded-xl bg-black/20 border border-white/10 text-white text-sm focus:outline-none focus:border-blue-500/50" />
                                            </div>
                                            <div>
                                                <label className="text-xs text-white/40 uppercase tracking-wider">Time Out</label>
                                                <input type="time" defaultValue={a.time_out || ''}
                                                    onBlur={e => markAttendance(a.staff_id, a.status, a.time_in, e.target.value)}
                                                    className="w-full mt-1 px-3 py-2 rounded-xl bg-black/20 border border-white/10 text-white text-sm focus:outline-none focus:border-blue-500/50" />
                                            </div>
                                        </div>
                                    ) : null}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
