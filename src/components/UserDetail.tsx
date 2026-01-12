import { X } from 'lucide-react';
import type { UserManagement } from '../lib/database.types';

interface UserDetailProps {
  isOpen: boolean;
  onClose: () => void;
  user: UserManagement | null;
}

// Mapping giữa giá trị DB và tên hiển thị
const GROUP_MAPPING: Record<string, string> = {
  'grp_admin': 'Admin',
  'grp_deds': 'Data Engineering & Science',
  'grp_de': 'Data Engineer',
  'grp_ds': 'Data Scientist',
};

export default function UserDetail({ isOpen, onClose, user }: UserDetailProps) {
  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-end">
      <div className="bg-white h-full w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col animate-slide-in">
        <div className="bg-gradient-to-r from-slate-700 to-slate-800 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">
            Xem chi tiết người dùng
          </h2>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="space-y-6">
            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <div className="w-1 h-4 bg-slate-600 rounded"></div>
                I. Thông tin tài khoản
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Tên đăng nhập
                  </label>
                  <input
                    type="text"
                    value={user.user_name}
                    disabled
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-700 cursor-not-allowed"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={user.email}
                    disabled
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-700 cursor-not-allowed"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Số điện thoại
                  </label>
                  <input
                    type="text"
                    value={user.phone_number || '-'}
                    disabled
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-700 cursor-not-allowed"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Trạng thái kích hoạt
                  </label>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        user.is_active
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-slate-100 text-slate-500 border border-slate-200'
                      }`}
                    >
                      {user.is_active ? 'Đang hoạt động' : 'Ngừng kích hoạt'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <div className="w-1 h-4 bg-slate-600 rounded"></div>
                II. Nhóm & Quyền
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Nhóm
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {user.group_names.length > 0 ? (
                      user.group_names.map((group, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium border border-slate-200"
                        >
                          {GROUP_MAPPING[group] || group}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-400">Chưa thuộc nhóm nào</span>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Quyền Zeppelin
                  </label>
                  <span
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                      user.zeppelin_role === 'admin'
                        ? 'bg-amber-50 text-amber-700 border border-amber-200'
                        : 'bg-sky-50 text-sky-700 border border-sky-200'
                    }`}
                  >
                    {user.zeppelin_role === 'admin' ? 'Admin' : 'User'}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <div className="w-1 h-4 bg-slate-600 rounded"></div>
                III. Bảo mật
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Danh sách IP
                  </label>
                  <textarea
                    value={user.ips.length > 0 ? user.ips.join('\n') : '-'}
                    disabled
                    rows={4}
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-700 cursor-not-allowed font-mono text-sm"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-600 mb-2">
                      Ngày tạo
                    </label>
                    <input
                      type="text"
                      value={new Date(user.created_date).toLocaleString('vi-VN')}
                      disabled
                      className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-500 cursor-not-allowed"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-600 mb-2">
                      Ngày cập nhật
                    </label>
                    <input
                      type="text"
                      value={new Date(user.updated_date).toLocaleString('vi-VN')}
                      disabled
                      className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-500 cursor-not-allowed"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-200 px-6 py-4 bg-slate-50 flex items-center justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-6 py-2.5 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-100 transition-colors font-medium"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
}
