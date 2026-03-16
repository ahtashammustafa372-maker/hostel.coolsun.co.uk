import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Search, ChevronLeft, ChevronRight, Activity, User, AlertTriangle } from 'lucide-react';

const API = '/api';

const actionColors = {
    CREATE: 'text-green-400 bg-green-500/10 border-green-500/20',
    UPDATE: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    DELETE: 'text-red-400 bg-red-500/10 border-red-500/20',
    APPROVE: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
    REJECT: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
    LOGIN: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
};

function getActionColor(action) {
    for (const key of Object.keys(actionColors)) {
        if (action?.includes(key)) return actionColors[key];
    }
    return 'text-white/50 bg-white/5 border-white/10';
}

export default function AuditLog() {
    const [logs, setLogs] = useState([]);
    const [total, setTotal] = useState(0);
    const [pages, setPages] = useState(1);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');

    const fetchLogs = async (p = 1) => {
        setLoading(true);
        try {
            const r = await axios.get(`${API}/audit/logs?page=${p}`);
            setLogs(r.data.logs || []);
            setTotal(r.data.total || 0);
            setPages(r.data.pages || 1);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchLogs(page); }, [page]);

    const filtered = search
        ? logs.filter(l =>
            l.action?.toLowerCase().includes(search.toLowerCase()) ||
            l.entity?.toLowerCase().includes(search.toLowerCase()) ||
            l.details?.toLowerCase().includes(search.toLowerCase())
        )
        : logs;

    return (
        <div className="p-6 space-y-6 max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Shield className="text-purple-400 w-7 h-7" /> Audit Log Vault
                    </h1>
                    <p className="text-white/50 text-sm mt-1">Immutable record of every action in the system</p>
                </div>
                <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/20">
                    <Activity className="w-4 h-4 text-purple-400" />
                    <span className="text-purple-300 text-sm font-medium">{total.toLocaleString()} total events</span>
                </div>
            </div>

            {/* Search */}
            <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 w-4 h-4" />
                <input type="text" value={search} onChange={e => setSearch(e.target.value)}
                    placeholder="Filter by action, entity, or details..."
                    className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-purple-500/50 text-sm" />
            </div>

            {/* Log Table */}
            <div className="rounded-2xl bg-white/5 border border-white/10 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead>
                            <tr className="bg-white/5 text-xs uppercase text-white/40 tracking-wider">
                                <th className="px-5 py-4">Timestamp</th>
                                <th className="px-5 py-4">Action</th>
                                <th className="px-5 py-4">Entity</th>
                                <th className="px-5 py-4">Details</th>
                                <th className="px-5 py-4">IP</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {loading ? (
                                <tr><td colSpan={5} className="text-center py-12 text-white/30">Loading audit logs...</td></tr>
                            ) : filtered.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="text-center py-12">
                                        <Shield className="w-10 h-10 mx-auto mb-3 text-white/10" />
                                        <p className="text-white/30 text-sm">No audit events recorded yet.</p>
                                        <p className="text-white/20 text-xs mt-1">Events are logged when staff perform actions like creating tenants, approving expenses, etc.</p>
                                    </td>
                                </tr>
                            ) : (
                                filtered.map(log => (
                                    <tr key={log.id} className="hover:bg-white/3 transition-colors">
                                        <td className="px-5 py-3 text-white/40 text-xs whitespace-nowrap font-mono">
                                            {log.timestamp ? new Date(log.timestamp).toLocaleString('en-PK', {
                                                dateStyle: 'short', timeStyle: 'short'
                                            }) : '—'}
                                        </td>
                                        <td className="px-5 py-3">
                                            <span className={`text-xs font-bold px-2 py-1 rounded-lg border ${getActionColor(log.action)}`}>
                                                {log.action}
                                            </span>
                                        </td>
                                        <td className="px-5 py-3 text-white/60 text-xs">
                                            {log.entity && (
                                                <span>{log.entity} {log.entity_id ? `#${log.entity_id}` : ''}</span>
                                            )}
                                        </td>
                                        <td className="px-5 py-3 text-white/50 text-xs max-w-xs truncate">{log.details || '—'}</td>
                                        <td className="px-5 py-3 text-white/30 text-xs font-mono">{log.ip_address || '—'}</td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Pagination */}
                {pages > 1 && (
                    <div className="flex items-center justify-between px-5 py-4 border-t border-white/5">
                        <span className="text-white/40 text-xs">Page {page} of {pages}</span>
                        <div className="flex gap-2">
                            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                                className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-white/50 text-xs disabled:opacity-30 transition-all flex items-center gap-1">
                                <ChevronLeft className="w-3 h-3" /> Prev
                            </button>
                            <button onClick={() => setPage(p => Math.min(pages, p + 1))} disabled={page === pages}
                                className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-white/50 text-xs disabled:opacity-30 transition-all flex items-center gap-1">
                                Next <ChevronRight className="w-3 h-3" />
                            </button>
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 rounded-2xl bg-yellow-500/5 border border-yellow-500/20 flex items-start gap-3">
                <AlertTriangle className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5" />
                <p className="text-yellow-300/70 text-xs">Audit logs are <strong>immutable</strong> — they cannot be edited or deleted. Every significant action like creating tenants, approving expenses, and updating fine types is automatically recorded here.</p>
            </div>
        </div>
    );
}
