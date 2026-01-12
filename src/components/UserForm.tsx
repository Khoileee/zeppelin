import { useState, useEffect } from 'react';
import { X, Eye, EyeOff, Info, AlertCircle } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { UserManagement } from '../lib/database.types';
import {
  validateEmail,
  validatePhoneNumber,
  validateIPList,
  generateUserName,
  generateShiroHash,
} from '../lib/validation';

interface UserFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editUser?: UserManagement | null;
}

// Mapping giữa giá trị DB và tên hiển thị
const GROUP_MAPPING: Record<string, string> = {
  'grp_admin': 'Admin',
  'grp_deds': 'Data Engineering & Science',
  'grp_de': 'Data Engineer',
  'grp_ds': 'Data Scientist',
};

const AVAILABLE_GROUPS = Object.keys(GROUP_MAPPING);

export default function UserForm({ isOpen, onClose, onSuccess, editUser }: UserFormProps) {
  const [formData, setFormData] = useState({
    user_name: '',
    email: '',
    phone_number: '',
    password: '',
    is_active: true,
    group_names: [] as string[],
    zeppelin_role: 'user' as 'admin' | 'user',
    ips: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
  } | null>(null);

  useEffect(() => {
    if (isOpen) {
      if (editUser) {
        setFormData({
          user_name: editUser.user_name,
          email: editUser.email,
          phone_number: editUser.phone_number || '',
          password: '',
          is_active: editUser.is_active,
          group_names: editUser.group_names,
          zeppelin_role: editUser.zeppelin_role,
          ips: editUser.ips.join('\n'),
        });
      } else {
        setFormData({
          user_name: generateUserName(),
          email: '',
          phone_number: '',
          password: '',
          is_active: true,
          group_names: [],
          zeppelin_role: 'user',
          ips: '',
        });
      }
      setErrors({});
      setNotification(null);
    }
  }, [isOpen, editUser]);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.user_name.trim()) {
      newErrors.user_name = 'Tên đăng nhập là bắt buộc';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email là bắt buộc';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Email không đúng định dạng';
    }

    if (formData.phone_number && !validatePhoneNumber(formData.phone_number)) {
      newErrors.phone_number = 'Số điện thoại không đúng định dạng (VD: 0912345678)';
    }

    if (!editUser && !formData.password) {
      newErrors.password = 'Mật khẩu là bắt buộc';
    }

    if (formData.password && formData.password.length < 6) {
      newErrors.password = 'Mật khẩu phải có ít nhất 6 ký tự';
    }

    if (formData.ips) {
      const ipValidation = validateIPList(formData.ips);
      if (!ipValidation.valid) {
        newErrors.ips = `IP không hợp lệ: ${ipValidation.invalidIPs.join(', ')}`;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      setNotification({
        type: 'error',
        message: 'Vui lòng kiểm tra lại các trường thông tin',
      });
      return;
    }

    setLoading(true);
    try {
      const ipsArray = formData.ips
        .split('\n')
        .map((ip) => ip.trim())
        .filter((ip) => ip.length > 0);

      if (editUser) {
        const updateData: any = {
          user_name: formData.user_name,
          email: formData.email,
          phone_number: formData.phone_number || null,
          is_active: formData.is_active,
          group_names: formData.group_names,
          zeppelin_role: formData.zeppelin_role,
          ips: ipsArray,
        };

        if (formData.password) {
          updateData.shiro_hash = await generateShiroHash(formData.password);
        }

        const { error } = await supabase
          .from('users_management')
          .update(updateData)
          .eq('user_id', editUser.user_id);

        if (error) throw error;

        setNotification({
          type: 'success',
          message: 'Cập nhật thông tin người dùng thành công',
        });
      } else {
        const shiroHash = await generateShiroHash(formData.password);
        const { error } = await supabase.from('users_management').insert({
          user_name: formData.user_name,
          email: formData.email,
          phone_number: formData.phone_number || null,
          shiro_hash: shiroHash,
          is_active: formData.is_active,
          group_names: formData.group_names,
          zeppelin_role: formData.zeppelin_role,
          ips: ipsArray,
        });

        if (error) {
          const pgError = error as { code?: string; message?: string };
          if (pgError.code === '23505') {
            if (pgError.message?.includes('user_name')) {
              throw new Error('Tên đăng nhập đã tồn tại');
            } else if (pgError.message?.includes('email')) {
              throw new Error('Email đã tồn tại');
            }
          }
          throw error;
        }

        setNotification({
          type: 'success',
          message: 'Thêm người dùng mới thành công',
        });
      }

      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1500);
    } catch (error: any) {
      setNotification({
        type: 'error',
        message: error.message || 'Có lỗi xảy ra, vui lòng thử lại',
      });
    } finally {
      setLoading(false);
    }
  };

  const toggleGroup = (group: string) => {
    setFormData((prev) => ({
      ...prev,
      group_names: prev.group_names.includes(group)
        ? prev.group_names.filter((g) => g !== group)
        : [...prev.group_names, group],
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-end">
      <div className="bg-white h-full w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col animate-slide-in">
        <div className="bg-gradient-to-r from-slate-700 to-slate-800 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">
            {editUser ? 'Chỉnh sửa người dùng' : 'Thêm người dùng mới'}
          </h2>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {notification && (
          <div
            className={`mx-6 mt-4 p-4 rounded-lg flex items-start gap-3 ${
              notification.type === 'success'
                ? 'bg-emerald-50 border border-emerald-200'
                : 'bg-rose-50 border border-rose-200'
            }`}
          >
            <AlertCircle
              size={20}
              className={notification.type === 'success' ? 'text-emerald-600' : 'text-rose-600'}
            />
            <p
              className={`text-sm ${
                notification.type === 'success' ? 'text-emerald-700' : 'text-rose-700'
              }`}
            >
              {notification.message}
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto px-6 py-6">
          <div className="space-y-6">
            <div className="bg-slate-50/50 rounded-xl p-5 border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <div className="w-1 h-4 bg-slate-600 rounded"></div>
                I. Thông tin tài khoản
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Tên đăng nhập <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.user_name}
                    onChange={(e) => setFormData({ ...formData, user_name: e.target.value })}
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white ${
                      errors.user_name ? 'border-rose-400' : 'border-slate-200'
                    }`}
                  />
                  {errors.user_name && (
                    <p className="mt-1 text-sm text-rose-600">{errors.user_name}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Email <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white ${
                      errors.email ? 'border-rose-400' : 'border-slate-200'
                    }`}
                  />
                  {errors.email && <p className="mt-1 text-sm text-rose-600">{errors.email}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Số điện thoại
                  </label>
                  <input
                    type="text"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                    placeholder="0912345678"
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none bg-white ${
                      errors.phone_number ? 'border-rose-400' : 'border-slate-200'
                    }`}
                  />
                  {errors.phone_number && (
                    <p className="mt-1 text-sm text-rose-600">{errors.phone_number}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2">
                    Mật khẩu {!editUser && <span className="text-rose-500">*</span>}
                    {editUser && <span className="text-slate-400 text-xs">(Để trống nếu không đổi)</span>}
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none pr-10 bg-white ${
                        errors.password ? 'border-rose-400' : 'border-slate-200'
                      }`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="mt-1 text-sm text-rose-600">{errors.password}</p>
                  )}
                </div>

                <div>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      className="w-4 h-4 text-slate-600 border-slate-300 rounded focus:ring-slate-500"
                    />
                    <span className="text-sm font-medium text-slate-600">
                      Trạng thái kích hoạt
                    </span>
                  </label>
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
                  <label className="block text-sm font-medium text-slate-600 mb-2 flex items-center gap-2">
                    Nhóm
                    <div className="group relative">
                      <Info size={14} className="text-slate-400 cursor-help" />
                      <div className="hidden group-hover:block absolute left-0 bottom-full mb-2 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                        Chọn một hoặc nhiều nhóm mà người dùng thuộc về
                      </div>
                    </div>
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {AVAILABLE_GROUPS.map((group) => (
                      <label key={group} className="flex items-center gap-2 cursor-pointer p-2.5 border border-slate-200 rounded-lg hover:bg-white hover:border-slate-300 transition-all bg-white/50">
                        <input
                          type="checkbox"
                          checked={formData.group_names.includes(group)}
                          onChange={() => toggleGroup(group)}
                          className="w-4 h-4 text-slate-600 border-slate-300 rounded focus:ring-slate-500"
                        />
                        <span className="text-sm text-slate-700">{GROUP_MAPPING[group]}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-2 flex items-center gap-2">
                    Quyền Zeppelin
                    <div className="group relative">
                      <Info size={14} className="text-slate-400 cursor-help" />
                      <div className="hidden group-hover:block absolute left-0 bottom-full mb-2 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                        Admin có toàn quyền, User có quyền hạn chế
                      </div>
                    </div>
                  </label>
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        checked={formData.zeppelin_role === 'user'}
                        onChange={() => setFormData({ ...formData, zeppelin_role: 'user' })}
                        className="w-4 h-4 text-slate-600 border-slate-300 focus:ring-slate-500"
                      />
                      <span className="text-sm text-slate-700">User</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        checked={formData.zeppelin_role === 'admin'}
                        onChange={() => setFormData({ ...formData, zeppelin_role: 'admin' })}
                        className="w-4 h-4 text-slate-600 border-slate-300 focus:ring-slate-500"
                      />
                      <span className="text-sm text-slate-700">Admin</span>
                    </label>
                  </div>
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
                  <label className="block text-sm font-medium text-slate-600 mb-2 flex items-center gap-2">
                    Danh sách IP
                    <div className="group relative">
                      <Info size={14} className="text-slate-400 cursor-help" />
                      <div className="hidden group-hover:block absolute left-0 bottom-full mb-2 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                        Nhập mỗi IP trên một dòng. VD: 192.168.1.1
                      </div>
                    </div>
                  </label>
                  <textarea
                    value={formData.ips}
                    onChange={(e) => setFormData({ ...formData, ips: e.target.value })}
                    placeholder="192.168.1.1&#10;192.168.1.2"
                    rows={4}
                    className={`w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-slate-400 focus:border-transparent outline-none font-mono text-sm bg-white ${
                      errors.ips ? 'border-rose-400' : 'border-slate-200'
                    }`}
                  />
                  {errors.ips && <p className="mt-1 text-sm text-rose-600">{errors.ips}</p>}
                </div>

                {editUser && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-600 mb-2">
                          Ngày tạo
                        </label>
                        <input
                          type="text"
                          value={new Date(editUser.created_date).toLocaleString('vi-VN')}
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
                          value={new Date(editUser.updated_date).toLocaleString('vi-VN')}
                          disabled
                          className="w-full px-4 py-2.5 border border-slate-200 rounded-lg bg-slate-100 text-slate-500 cursor-not-allowed"
                        />
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </form>

        <div className="border-t border-slate-200 px-6 py-4 bg-slate-50 flex items-center justify-end">
          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2.5 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-100 transition-colors font-medium"
            >
              Hủy
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="px-6 py-2.5 bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg hover:from-slate-800 hover:to-slate-900 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-sm"
            >
              {loading ? 'Đang lưu...' : 'Lưu'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
