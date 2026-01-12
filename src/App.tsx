import { useState } from 'react';
import { Users, UserPlus } from 'lucide-react';
import UserList from './components/UserList';
import UserForm from './components/UserForm';
import UserDetail from './components/UserDetail';
import type { UserManagement } from './lib/database.types';

function App() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [editUser, setEditUser] = useState<UserManagement | null>(null);
  const [viewUser, setViewUser] = useState<UserManagement | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAddUser = () => {
    setEditUser(null);
    setIsFormOpen(true);
  };

  const handleEditUser = (user: UserManagement) => {
    setEditUser(user);
    setIsFormOpen(true);
  };

  const handleViewUser = (user: UserManagement) => {
    setViewUser(user);
    setIsDetailOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditUser(null);
  };

  const handleCloseDetail = () => {
    setIsDetailOpen(false);
    setViewUser(null);
  };

  const handleSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl shadow-lg">
              <Users size={28} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-800">
                Quản lý người dùng
              </h1>
              <p className="text-slate-500 mt-1">
                Quản lý danh sách người dùng hệ thống nội bộ
              </p>
            </div>
          </div>
          <button
            onClick={handleAddUser}
            className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg hover:from-slate-800 hover:to-slate-900 transition-all shadow-sm"
          >
            <UserPlus size={18} />
            <span>Thêm người dùng</span>
          </button>
        </div>

        <UserList
          onAddUser={handleAddUser}
          onEditUser={handleEditUser}
          onViewUser={handleViewUser}
          refreshTrigger={refreshTrigger}
        />

        <UserForm
          isOpen={isFormOpen}
          onClose={handleCloseForm}
          onSuccess={handleSuccess}
          editUser={editUser}
        />

        <UserDetail
          isOpen={isDetailOpen}
          onClose={handleCloseDetail}
          user={viewUser}
        />
      </div>
    </div>
  );
}

export default App;
