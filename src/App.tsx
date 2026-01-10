import { useState } from 'react';
import { Users } from 'lucide-react';
import UserList from './components/UserList';
import UserForm from './components/UserForm';
import type { UserManagement } from './lib/database.types';

function App() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editUser, setEditUser] = useState<UserManagement | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAddUser = () => {
    setEditUser(null);
    setIsFormOpen(true);
  };

  const handleEditUser = (user: UserManagement) => {
    setEditUser(user);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setEditUser(null);
  };

  const handleSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
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
        </div>

        <UserList
          onAddUser={handleAddUser}
          onEditUser={handleEditUser}
          refreshTrigger={refreshTrigger}
        />

        <UserForm
          isOpen={isFormOpen}
          onClose={handleCloseForm}
          onSuccess={handleSuccess}
          editUser={editUser}
        />
      </div>
    </div>
  );
}

export default App;
