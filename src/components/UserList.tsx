import { useState, useEffect } from 'react';
import { Search, Filter, UserPlus, Edit2, Power, PowerOff, AlertTriangle, X, RotateCcw, ChevronLeft, ChevronRight } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { UserManagement } from '../lib/database.types';

// Fake data
const FAKE_USERS: UserManagement[] = [
  {
    user_id: 'fake-1',
    user_name: 'usr_khoiln1',
    email: 'khoiln1@company.com',
    phone_number: '0901234567',
    is_active: true,
    group_names: ['grp_de'],
    zeppelin_role: 'user',
    ips: ['192.168.1.10'],
    shiro_hash: '$shiro1$SHA-256$500000$fake1',
    created_date: '2025-12-15T08:30:00Z',
    updated_date: '2025-12-20T10:00:00Z',
  },
  {
    user_id: 'fake-2',
    user_name: 'usr_anhhv13',
    email: 'anhhv13@company.com',
    phone_number: '0912345678',
    is_active: true,
    group_names: ['grp_ds'],
    zeppelin_role: 'user',
    ips: ['192.168.1.11'],
    shiro_hash: '$shiro1$SHA-256$500000$fake2',
    created_date: '2025-11-20T09:15:00Z',
    updated_date: '2025-12-01T14:30:00Z',
  },
  {
    user_id: 'fake-3',
    user_name: 'usr_hangttm9',
    email: 'hangttm9@company.com',
    phone_number: '0923456789',
    is_active: true,
    group_names: ['grp_deds'],
    zeppelin_role: 'admin',
    ips: ['192.168.1.12'],
    shiro_hash: '$shiro1$SHA-256$500000$fake3',
    created_date: '2025-10-10T10:00:00Z',
    updated_date: '2025-11-15T16:45:00Z',
  },
  {
    user_id: 'fake-4',
    user_name: 'usr_baont12',
    email: 'baont12@company.com',
    phone_number: '0934567890',
    is_active: false,
    group_names: ['grp_de', 'grp_ds'],
    zeppelin_role: 'user',
    ips: ['192.168.1.13'],
    shiro_hash: '$shiro1$SHA-256$500000$fake4',
    created_date: '2025-09-05T11:30:00Z',
    updated_date: '2025-10-20T09:00:00Z',
  },
  {
    user_id: 'fake-5',
    user_name: 'usr_quanpd9',
    email: 'quanpd9@company.com',
    phone_number: '0945678901',
    is_active: true,
    group_names: ['grp_admin'],
    zeppelin_role: 'admin',
    ips: ['192.168.1.14', '10.0.0.5'],
    shiro_hash: '$shiro1$SHA-256$500000$fake5',
    created_date: '2025-08-12T14:00:00Z',
    updated_date: '2025-09-25T11:20:00Z',
  },
  {
    user_id: 'fake-6',
    user_name: 'usr_toancv2',
    email: 'toancv2@company.com',
    phone_number: '0956789012',
    is_active: true,
    group_names: ['grp_de'],
    zeppelin_role: 'user',
    ips: ['192.168.1.15'],
    shiro_hash: '$shiro1$SHA-256$500000$fake6',
    created_date: '2025-07-18T08:45:00Z',
    updated_date: '2025-08-30T13:15:00Z',
  },
  {
    user_id: 'fake-7',
    user_name: 'usr_sonnh70',
    email: 'sonnh70@company.com',
    phone_number: '0967890123',
    is_active: true,
    group_names: ['grp_ds'],
    zeppelin_role: 'user',
    ips: ['192.168.1.16'],
    shiro_hash: '$shiro1$SHA-256$500000$fake7',
    created_date: '2025-06-22T09:30:00Z',
    updated_date: '2025-07-10T15:00:00Z',
  },
  {
    user_id: 'fake-8',
    user_name: 'usr_linhnt5',
    email: 'linhnt5@company.com',
    phone_number: '0978901234',
    is_active: false,
    group_names: ['grp_deds'],
    zeppelin_role: 'user',
    ips: ['192.168.1.17'],
    shiro_hash: '$shiro1$SHA-256$500000$fake8',
    created_date: '2025-05-14T10:15:00Z',
    updated_date: '2025-06-05T12:30:00Z',
  },
  {
    user_id: 'fake-9',
    user_name: 'usr_dungpv8',
    email: 'dungpv8@company.com',
    phone_number: '0989012345',
    is_active: true,
    group_names: ['grp_de', 'grp_admin'],
    zeppelin_role: 'admin',
    ips: ['192.168.1.18'],
    shiro_hash: '$shiro1$SHA-256$500000$fake9',
    created_date: '2025-04-08T07:00:00Z',
    updated_date: '2025-05-20T08:45:00Z',
  },
  {
    user_id: 'fake-10',
    user_name: 'usr_thuydth3',
    email: 'thuydth3@company.com',
    phone_number: '0990123456',
    is_active: true,
    group_names: ['grp_ds'],
    zeppelin_role: 'user',
    ips: ['192.168.1.19'],
    shiro_hash: '$shiro1$SHA-256$500000$fake10',
    created_date: '2025-03-25T11:45:00Z',
    updated_date: '2025-04-15T10:00:00Z',
  },
];

// Mapping giữa giá trị DB và tên hiển thị
const GROUP_MAPPING: Record<string, string> = {
  'grp_admin': 'Admin',
  'grp_deds': 'Data Engineering & Science',
  'grp_de': 'Data Engineer',
  'grp_ds': 'Data Scientist',
};

interface UserListProps {
  onAddUser: () => void;
  onEditUser: (user: UserManagement) => void;
  refreshTrigger: number;
}

export default function UserList({ onAddUser, onEditUser, refreshTrigger }: UserListProps) {
  const [users, setUsers] = useState<UserManagement[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<UserManagement[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [groupFilter, setGroupFilter] = useState('');
  const [roleFilter, setRoleFilter] = useState<'all' | 'admin' | 'user'>('all');
  const [dateFromFilter, setDateFromFilter] = useState('');
  const [dateToFilter, setDateToFilter] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    user: UserManagement | null;
  }>({ isOpen: false, user: null });

  useEffect(() => {
    fetchUsers();
  }, [refreshTrigger]);

  useEffect(() => {
    applyFilters();
  }, [users, searchTerm, statusFilter, groupFilter, roleFilter, dateFromFilter, dateToFilter]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('users_management')
        .select('*')
        .order('created_date', { ascending: false });

      if (error) throw error;
      // Kết hợp dữ liệu thực với fake data
      const allUsers = [...(data || []), ...FAKE_USERS];
      // Sắp xếp theo ngày tạo giảm dần
      allUsers.sort((a, b) => new Date(b.created_date).getTime() - new Date(a.created_date).getTime());
      setUsers(allUsers);
    } catch (error) {
      console.error('Lỗi khi tải danh sách người dùng:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...users];

    if (searchTerm) {
      filtered = filtered.filter(user =>
        user.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.phone_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.group_names.some(group => group.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(user =>
        statusFilter === 'active' ? user.is_active : !user.is_active
      );
    }

    if (groupFilter) {
      filtered = filtered.filter(user =>
        user.group_names.some(group => group.toLowerCase().includes(groupFilter.toLowerCase()))
      );
    }

    if (roleFilter !== 'all') {
      filtered = filtered.filter(user => user.zeppelin_role === roleFilter);
    }

    if (dateFromFilter) {
      const fromDate = new Date(dateFromFilter);
      fromDate.setHours(0, 0, 0, 0);
      filtered = filtered.filter(user => new Date(user.created_date) >= fromDate);
    }

    if (dateToFilter) {
      const toDate = new Date(dateToFilter);
      toDate.setHours(23, 59, 59, 999);
      filtered = filtered.filter(user => new Date(user.created_date) <= toDate);
    }

    setFilteredUsers(filtered);
    setCurrentPage(1);
  };

  const openConfirmDialog = (user: UserManagement) => {
    setConfirmDialog({ isOpen: true, user });
  };

  const closeConfirmDialog = () => {
    setConfirmDialog({ isOpen: false, user: null });
  };

  const confirmToggleStatus = async () => {
    if (!confirmDialog.user) return;
    
    try {
      const { error } = await supabase
        .from('users_management')
        .update({ is_active: !confirmDialog.user.is_active })
        .eq('user_id', confirmDialog.user.user_id);

      if (error) throw error;
      fetchUsers();
    } catch (error) {
      console.error('Lỗi khi cập nhật trạng thái:', error);
    } finally {
      closeConfirmDialog();
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
          <div className="flex-1 w-full md:w-auto">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Tìm kiếm theo tên, email, nhóm, số điện thoại..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none transition-all bg-white"
              />
            </div>
          </div>

          <div className="flex gap-2 w-full md:w-auto">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-4 py-2.5 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-slate-600"
            >
              <Filter size={18} />
              <span>Bộ lọc</span>
            </button>
          </div>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-slate-200 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-2">
                Trạng thái hoạt động
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white"
              >
                <option value="all">Tất cả</option>
                <option value="active">Đang hoạt động</option>
                <option value="inactive">Ngừng kích hoạt</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-600 mb-2">
                Nhóm
              </label>
              <input
                type="text"
                placeholder="Lọc theo nhóm..."
                value={groupFilter}
                onChange={(e) => setGroupFilter(e.target.value)}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-600 mb-2">
                Quyền Zeppelin
              </label>
              <select
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white"
              >
                <option value="all">Tất cả</option>
                <option value="admin">Admin</option>
                <option value="user">User</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-600 mb-2">
                Ngày tạo
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="date"
                  value={dateFromFilter}
                  onChange={(e) => setDateFromFilter(e.target.value)}
                  className="flex-1 px-2 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white text-sm"
                />
                <span className="text-slate-400 text-sm">-</span>
                <input
                  type="date"
                  value={dateToFilter}
                  onChange={(e) => setDateToFilter(e.target.value)}
                  className="flex-1 px-2 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white text-sm"
                />
              </div>
            </div>

            <div className="flex items-end gap-2 md:col-span-4 justify-end mt-2">
              <button
                onClick={() => {
                  setSearchTerm('');
                  setStatusFilter('all');
                  setGroupFilter('');
                  setRoleFilter('all');
                  setDateFromFilter('');
                  setDateToFilter('');
                }}
                className="flex items-center gap-2 px-4 py-2 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors text-slate-600"
              >
                <RotateCcw size={16} />
                <span>Làm mới</span>
              </button>
              <button
                onClick={() => applyFilters()}
                className="flex items-center gap-2 px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800 transition-colors"
              >
                <Search size={16} />
                <span>Tìm kiếm</span>
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500">
            Đang tải dữ liệu...
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="p-8 text-center text-slate-500">
            Không tìm thấy người dùng nào
          </div>
        ) : (
          <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200 sticky top-0 z-10">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    STT
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Tên đăng nhập
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Số điện thoại
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Nhóm
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Quyền
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Trạng thái
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Ngày tạo
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Ngày cập nhật
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Hành động
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredUsers
                  .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
                  .map((user, index) => (
                  <tr
                    key={user.user_id}
                    className="hover:bg-slate-50/50 transition-colors"
                  >
                    <td className="px-4 py-3 text-sm text-slate-500">
                      {(currentPage - 1) * itemsPerPage + index + 1}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-slate-800">
                      {user.user_name}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {user.email}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {user.phone_number || '-'}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex flex-wrap gap-1">
                        {user.group_names.length > 0 ? (
                          user.group_names.map((group, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs font-medium"
                            >
                              {GROUP_MAPPING[group] || group}
                            </span>
                          ))
                        ) : (
                          <span className="text-slate-400">-</span>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium ${
                          user.zeppelin_role === 'admin'
                            ? 'bg-amber-50 text-amber-700 border border-amber-200'
                            : 'bg-sky-50 text-sky-700 border border-sky-200'
                        }`}
                      >
                        {user.zeppelin_role}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium ${
                          user.is_active
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-slate-100 text-slate-500 border border-slate-200'
                        }`}
                      >
                        {user.is_active ? 'Đang hoạt động' : 'Ngừng kích hoạt'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {formatDate(user.created_date)}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {formatDate(user.updated_date)}
                    </td>
                    <td className="px-4 py-3 text-sm text-right">
                      <div className="flex items-center justify-end gap-1">
                        <button
                          onClick={() => onEditUser(user)}
                          className="p-1.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
                          title="Chỉnh sửa"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => openConfirmDialog(user)}
                          className={`p-1.5 rounded-lg transition-colors ${
                            user.is_active
                              ? 'text-rose-500 hover:text-rose-700 hover:bg-rose-50'
                              : 'text-emerald-500 hover:text-emerald-700 hover:bg-emerald-50'
                          }`}
                          title={user.is_active ? 'Ngừng kích hoạt' : 'Kích hoạt lại'}
                        >
                          {user.is_active ? <PowerOff size={16} /> : <Power size={16} />}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {filteredUsers.length > 0 && (
        <div className="flex items-center justify-end gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-600">Hiển thị</span>
            <select
              value={itemsPerPage}
              onChange={(e) => {
                setItemsPerPage(Number(e.target.value));
                setCurrentPage(1);
              }}
              className="px-2 py-1.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white text-sm"
            >
              <option value={10}>10</option>
              <option value={15}>15</option>
              <option value={20}>20</option>
            </select>
            <span className="text-sm text-slate-600">bản ghi</span>
          </div>
          <span className="text-sm text-slate-600">
            {Math.min((currentPage - 1) * itemsPerPage + 1, filteredUsers.length)} - {Math.min(currentPage * itemsPerPage, filteredUsers.length)} / {filteredUsers.length}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="p-2 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft size={18} className="text-slate-600" />
            </button>
            {Array.from({ length: Math.ceil(filteredUsers.length / itemsPerPage) }, (_, i) => i + 1).map(page => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-3 py-1.5 rounded-lg transition-colors text-sm font-medium ${
                  currentPage === page
                    ? 'bg-slate-700 text-white'
                    : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                {page}
              </button>
            ))}
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, Math.ceil(filteredUsers.length / itemsPerPage)))}
              disabled={currentPage === Math.ceil(filteredUsers.length / itemsPerPage)}
              className="p-2 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight size={18} className="text-slate-600" />
            </button>
          </div>
        </div>
      )}

      {/* Confirmation Dialog */}
      {confirmDialog.isOpen && confirmDialog.user && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full mx-4 overflow-hidden border border-slate-200">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
              <h3 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                <AlertTriangle className={confirmDialog.user.is_active ? 'text-rose-500' : 'text-emerald-500'} size={20} />
                Xác nhận {confirmDialog.user.is_active ? 'ngừng kích hoạt' : 'kích hoạt'}
              </h3>
              <button
                onClick={closeConfirmDialog}
                className="text-slate-400 hover:text-slate-600 transition-colors p-1 hover:bg-slate-100 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>
            <div className="px-6 py-5">
              <p className="text-slate-600">
                Bạn có chắc chắn muốn{' '}
                <span className={`font-semibold ${confirmDialog.user.is_active ? 'text-rose-600' : 'text-emerald-600'}`}>
                  {confirmDialog.user.is_active ? 'ngừng kích hoạt' : 'kích hoạt lại'}
                </span>{' '}
                người dùng{' '}
                <span className="font-semibold text-slate-800">{confirmDialog.user.user_name}</span>?
              </p>
              {confirmDialog.user.is_active && (
                <p className="mt-2 text-sm text-slate-500">
                  Người dùng sẽ không thể đăng nhập sau khi bị ngừng kích hoạt.
                </p>
              )}
            </div>
            <div className="px-6 py-4 bg-slate-50 flex justify-end gap-3 border-t border-slate-100">
              <button
                onClick={closeConfirmDialog}
                className="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-100 transition-colors font-medium"
              >
                Hủy
              </button>
              <button
                onClick={confirmToggleStatus}
                className={`px-4 py-2 text-white rounded-lg transition-colors font-medium ${
                  confirmDialog.user.is_active
                    ? 'bg-rose-500 hover:bg-rose-600'
                    : 'bg-emerald-500 hover:bg-emerald-600'
                }`}
              >
                {confirmDialog.user.is_active ? 'Ngừng kích hoạt' : 'Kích hoạt'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
