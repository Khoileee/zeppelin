import type { UserManagement } from './database.types';

const STORAGE_KEY = 'users_management';

// Khởi tạo dữ liệu mẫu nếu chưa có
const initializeStorage = (): UserManagement[] => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    return JSON.parse(stored);
  }
  
  // Dữ liệu mẫu ban đầu
  const sampleData: UserManagement[] = [
    {
      user_id: crypto.randomUUID(),
      user_name: 'admin_demo',
      email: 'admin@example.com',
      phone_number: '0912345678',
      is_active: true,
      group_names: ['grp_admin'],
      zeppelin_role: 'admin',
      ips: ['192.168.1.1'],
      shiro_hash: '$shiro1$SHA-256$500000$demo',
      created_date: new Date().toISOString(),
      updated_date: new Date().toISOString(),
    },
    {
      user_id: crypto.randomUUID(),
      user_name: 'user_de_01',
      email: 'de01@example.com',
      phone_number: '0987654321',
      is_active: true,
      group_names: ['grp_de', 'grp_deds'],
      zeppelin_role: 'user',
      ips: [],
      shiro_hash: '$shiro1$SHA-256$500000$demo',
      created_date: new Date().toISOString(),
      updated_date: new Date().toISOString(),
    },
  ];
  
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sampleData));
  return sampleData;
};

// Lấy tất cả users
const getAll = (): UserManagement[] => {
  return initializeStorage();
};

// Lưu tất cả users
const saveAll = (users: UserManagement[]): void => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
};

// Tạo UUID
const generateUUID = (): string => {
  return crypto.randomUUID();
};

// Giả lập Supabase client interface
export const storage = {
  from: (_table: string) => ({
    select: (_columns?: string) => ({
      order: (_column: string, options?: { ascending: boolean }) => {
        return new Promise<{ data: UserManagement[] | null; error: Error | null }>((resolve) => {
          setTimeout(() => {
            let users = getAll();
            if (options?.ascending === false) {
              users = users.sort((a, b) => 
                new Date(b.created_date).getTime() - new Date(a.created_date).getTime()
              );
            }
            resolve({ data: users, error: null });
          }, 100);
        });
      },
    }),
    insert: (data: Partial<UserManagement> | Partial<UserManagement>[]) => {
      return new Promise<{ data: UserManagement | null; error: Error | null }>((resolve) => {
        setTimeout(() => {
          const users = getAll();
          const newUser = Array.isArray(data) ? data[0] : data;
          
          // Kiểm tra trùng user_name
          if (users.some(u => u.user_name === newUser.user_name)) {
            resolve({ 
              data: null, 
              error: Object.assign(new Error('Tên đăng nhập đã tồn tại'), { code: '23505', message: 'user_name already exists' })
            });
            return;
          }
          
          // Kiểm tra trùng email
          if (users.some(u => u.email === newUser.email)) {
            resolve({ 
              data: null, 
              error: Object.assign(new Error('Email đã tồn tại'), { code: '23505', message: 'email already exists' })
            });
            return;
          }
          
          const user: UserManagement = {
            user_id: generateUUID(),
            user_name: newUser.user_name || '',
            email: newUser.email || '',
            phone_number: newUser.phone_number || null,
            is_active: newUser.is_active ?? true,
            group_names: newUser.group_names || [],
            zeppelin_role: newUser.zeppelin_role || 'user',
            ips: newUser.ips || [],
            shiro_hash: newUser.shiro_hash || '',
            created_date: new Date().toISOString(),
            updated_date: new Date().toISOString(),
          };
          
          users.push(user);
          saveAll(users);
          resolve({ data: user, error: null });
        }, 100);
      });
    },
    update: (data: Partial<UserManagement>) => ({
      eq: (_column: string, value: string) => {
        return new Promise<{ data: UserManagement | null; error: Error | null }>((resolve) => {
          setTimeout(() => {
            const users = getAll();
            const index = users.findIndex(u => u.user_id === value);
            
            if (index === -1) {
              resolve({ data: null, error: new Error('Không tìm thấy người dùng') });
              return;
            }
            
            // Kiểm tra trùng user_name với user khác
            if (data.user_name && users.some(u => u.user_name === data.user_name && u.user_id !== value)) {
              resolve({ 
                data: null, 
                error: Object.assign(new Error('Tên đăng nhập đã tồn tại'), { code: '23505', message: 'user_name already exists' })
              });
              return;
            }
            
            // Kiểm tra trùng email với user khác
            if (data.email && users.some(u => u.email === data.email && u.user_id !== value)) {
              resolve({ 
                data: null, 
                error: Object.assign(new Error('Email đã tồn tại'), { code: '23505', message: 'email already exists' })
              });
              return;
            }
            
            users[index] = {
              ...users[index],
              ...data,
              updated_date: new Date().toISOString(),
            };
            
            saveAll(users);
            resolve({ data: users[index], error: null });
          }, 100);
        });
      },
    }),
    delete: () => ({
      eq: (_column: string, value: string) => {
        return new Promise<{ data: null; error: Error | null }>((resolve) => {
          setTimeout(() => {
            const users = getAll();
            const filtered = users.filter(u => u.user_id !== value);
            saveAll(filtered);
            resolve({ data: null, error: null });
          }, 100);
        });
      },
    }),
  }),
};

// Export với tên supabase để tương thích với code hiện tại
export const supabase = storage;
