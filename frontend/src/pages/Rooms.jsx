import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LayoutDashboard, Edit3, Users, Home, AlertCircle, Save, X, Trash2 } from 'lucide-react';
import axios from 'axios';

const Rooms = () => {
    const [rooms, setRooms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editingRoom, setEditingRoom] = useState(null);
    const [isAddingRoom, setIsAddingRoom] = useState(false);
    const [newRoom, setNewRoom] = useState({ number: '', floor: 1, type: 'Small', capacity: 2, base_rent: 10000 });
    const [error, setError] = useState(null);

    const fetchRooms = async () => {
        try {
            const res = await axios.get('/api/rooms');
            setRooms(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch rooms", err);
            setError("Could not load room inventory.");
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRooms();
    }, []);

    const handleUpdate = async (e) => {
        e.preventDefault();
        try {
            await axios.put(`/api/rooms/${editingRoom.id}`, editingRoom);
            setEditingRoom(null);
            fetchRooms();
        } catch (err) {
            const msg = err.response?.data?.message || err.response?.data?.error || "Update failed";
            alert(msg);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/rooms', newRoom);
            setIsAddingRoom(false);
            setNewRoom({ number: '', floor: 1, type: 'Small', capacity: 2, base_rent: 10000 });
            fetchRooms();
        } catch (err) {
            const errorMsg = err.response?.data?.message || err.response?.data?.error || "Failed to create room: Check required fields";
            alert(errorMsg);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this room?")) return;
        try {
            await axios.delete(`/api/rooms/${id}`);
            setEditingRoom(null);
            fetchRooms();
        } catch (err) {
            alert(err.response?.data?.error || "Failed to delete room");
        }
    };

    if (loading) return <div className="p-8 text-white/50 animate-pulse">Scanning Grid...</div>;

    return (
        <div className="space-y-8">
            <header className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">Room Inventory</h1>
                    <p className="text-white/40 text-sm mt-1">Configure property layout and pricing</p>
                </div>
                <div className="flex items-center space-x-4">
                    <div className="px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg text-blue-400 text-xs font-mono uppercase">
                        Total Rooms: {rooms.length}
                    </div>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setIsAddingRoom(true)}
                        className="px-4 py-2 bg-green-600 hover:bg-green-500 text-white text-sm font-medium rounded-lg transition-all shadow-lg shadow-green-500/20"
                    >
                        + Add Room
                    </motion.button>
                </div>
            </header>

            {error && (
                <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-xl text-red-400 flex items-center">
                    <AlertCircle size={18} className="mr-2" /> {error}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {rooms.map(room => (
                    <motion.div
                        key={room.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card p-6 border-white/5 bg-white/[0.02] flex flex-col justify-between group"
                    >
                        <div>
                            <div className="flex justify-between items-start mb-4">
                                <div className={`h-12 w-12 rounded-xl flex items-center justify-center font-bold text-lg ${room.available_slots > 0 ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' : 'bg-white/10 text-white/40'
                                    }`}>
                                    {room.number}
                                </div>
                                <button
                                    onClick={() => setEditingRoom(room)}
                                    className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-white/30 hover:text-white transition-all opacity-0 group-hover:opacity-100"
                                >
                                    <Edit3 size={18} />
                                </button>
                            </div>

                            <div className="space-y-3">
                                <div className="flex justify-between text-sm">
                                    <span className="text-white/40 uppercase tracking-wider text-[10px]">Type</span>
                                    <span className="text-white font-medium">{room.type}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-white/40 uppercase tracking-wider text-[10px]">Base Rent</span>
                                    <span className="text-blue-400 font-bold">Rs. {room.base_rent.toLocaleString()}</span>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 pt-6 border-t border-white/5">
                            <div className="flex justify-between items-end mb-2">
                                <p className="text-[10px] text-white/40 uppercase tracking-widest">Occupancy</p>
                                <p className="text-xs font-medium text-white">{room.occupied_beds} / {room.capacity}</p>
                            </div>
                            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                                <div
                                    className={`h-full transition-all duration-500 ${room.available_slots === 0 ? 'bg-red-500' : 'bg-blue-500'
                                        }`}
                                    style={{ width: `${(room.occupied_beds / room.capacity) * 100}%` }}
                                />
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Edit Modal */}
            <AnimatePresence>
                {editingRoom && (
                    <div className="fixed inset-0 z-[110] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setEditingRoom(null)}
                            className="absolute inset-0 bg-black/80 backdrop-blur-md"
                        />
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="glass-card w-full max-w-md p-8 border-blue-500/30 shadow-2xl relative z-[111] pointer-events-auto"
                        >
                            <div className="flex justify-between items-center mb-8">
                                <h3 className="text-xl font-bold text-white flex items-center">
                                    <Home size={20} className="mr-3 text-blue-400" /> Configure Room {editingRoom.number}
                                </h3>
                                <button onClick={() => setEditingRoom(null)} className="text-white/30 hover:text-white transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <form onSubmit={handleUpdate} className="space-y-6">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Room Number</label>
                                        <input
                                            type="text"
                                            value={editingRoom.number}
                                            onChange={e => setEditingRoom({ ...editingRoom, number: e.target.value })}
                                            className="glass-input w-full h-12 px-4 rounded-xl"
                                        />
                                    </div>
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Type</label>
                                        <select
                                            value={editingRoom.type}
                                            onChange={e => setEditingRoom({ ...editingRoom, type: e.target.value })}
                                            className="glass-input w-full h-12 px-4 rounded-xl appearance-none"
                                        >
                                            <option value="Small">Small</option>
                                            <option value="Medium">Medium</option>
                                            <option value="Large">Large</option>
                                        </select>
                                    </div>
                                </div>

                                <div>
                                    <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Base Monthly Rent (Rs)</label>
                                    <input
                                        type="number"
                                        value={editingRoom.base_rent}
                                        onChange={e => setEditingRoom({ ...editingRoom, base_rent: e.target.value })}
                                        className="glass-input w-full h-12 px-4 rounded-xl text-blue-400 font-bold"
                                    />
                                </div>

                                <div>
                                    <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold flex justify-between">
                                        Total Capacity
                                        <span className="text-white/20 font-normal">Active Tenants: {editingRoom.occupied_beds}</span>
                                    </label>
                                    <input
                                        type="number"
                                        value={editingRoom.capacity}
                                        min={editingRoom.occupied_beds}
                                        onChange={e => setEditingRoom({ ...editingRoom, capacity: parseInt(e.target.value) })}
                                        className="glass-input w-full h-12 px-4 rounded-xl"
                                    />
                                    {editingRoom.capacity < editingRoom.occupied_beds && (
                                        <p className="text-red-400 text-[10px] mt-2 flex items-center">
                                            <AlertCircle size={10} className="mr-1" /> Cannot reduce below current tenants
                                        </p>
                                    )}
                                </div>

                                <div className="flex space-x-4 mt-4">
                                    <button
                                        type="button"
                                        onClick={() => handleDelete(editingRoom.id)}
                                        className="py-4 px-6 bg-red-600/20 hover:bg-red-600/40 text-red-500 rounded-xl font-bold transition-all border border-red-500/30"
                                        title="Delete Room"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                    <button
                                        disabled={editingRoom.capacity < editingRoom.occupied_beds}
                                        type="submit"
                                        className="flex-1 py-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:hover:bg-blue-600 text-white rounded-xl font-bold flex items-center justify-center transition-all shadow-lg shadow-blue-500/30"
                                    >
                                        <Save size={18} className="mr-2" /> Save Configuration
                                    </button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}

                {/* Add Room Modal */}
                {isAddingRoom && (
                    <div className="fixed inset-0 z-[110] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsAddingRoom(false)}
                            className="absolute inset-0 bg-black/80 backdrop-blur-md"
                        />
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="glass-card w-full max-w-md p-8 border-green-500/30 shadow-2xl relative z-[111] pointer-events-auto"
                        >
                            <div className="flex justify-between items-center mb-8">
                                <h3 className="text-xl font-bold text-white flex items-center">
                                    <Home size={20} className="mr-3 text-green-400" /> Add New Room
                                </h3>
                                <button onClick={() => setIsAddingRoom(false)} className="text-white/30 hover:text-white transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <form onSubmit={handleCreate} className="space-y-6">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Room Number *</label>
                                        <input
                                            required
                                            type="text"
                                            value={newRoom.number}
                                            onChange={e => setNewRoom({ ...newRoom, number: e.target.value })}
                                            className="glass-input w-full h-12 px-4 rounded-xl"
                                        />
                                    </div>
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Floor</label>
                                        <input
                                            required
                                            type="number"
                                            value={newRoom.floor}
                                            onChange={e => setNewRoom({ ...newRoom, floor: parseInt(e.target.value) })}
                                            className="glass-input w-full h-12 px-4 rounded-xl"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Type</label>
                                        <select
                                            value={newRoom.type}
                                            onChange={e => setNewRoom({ ...newRoom, type: e.target.value })}
                                            className="glass-input w-full h-12 px-4 rounded-xl appearance-none"
                                        >
                                            <option value="Small">Small</option>
                                            <option value="Medium">Medium</option>
                                            <option value="Large">Large</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold flex justify-between">Capacity</label>
                                        <input
                                            required
                                            type="number"
                                            value={newRoom.capacity}
                                            min="1"
                                            onChange={e => setNewRoom({ ...newRoom, capacity: parseInt(e.target.value) })}
                                            className="glass-input w-full h-12 px-4 rounded-xl"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="text-[10px] text-white/40 uppercase tracking-widest mb-2 block font-bold">Base Monthly Rent (Rs)</label>
                                    <input
                                        required
                                        type="number"
                                        value={newRoom.base_rent}
                                        onChange={e => setNewRoom({ ...newRoom, base_rent: e.target.value })}
                                        className="glass-input w-full h-12 px-4 rounded-xl text-green-400 font-bold"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="w-full py-4 mt-4 bg-green-600 hover:bg-green-500 text-white rounded-xl font-bold flex items-center justify-center transition-all shadow-lg shadow-green-500/30"
                                >
                                    <Save size={18} className="mr-2" /> Create Room
                                </button>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Rooms;
