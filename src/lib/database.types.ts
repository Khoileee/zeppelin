export interface Database {
  public: {
    Tables: {
      users_management: {
        Row: {
          user_id: string;
          user_name: string;
          email: string;
          phone_number: string | null;
          is_active: boolean;
          group_names: string[];
          zeppelin_role: 'admin' | 'user';
          ips: string[];
          shiro_hash: string;
          created_date: string;
          updated_date: string;
        };
        Insert: {
          user_id?: string;
          user_name: string;
          email: string;
          phone_number?: string | null;
          is_active?: boolean;
          group_names?: string[];
          zeppelin_role?: 'admin' | 'user';
          ips?: string[];
          shiro_hash: string;
          created_date?: string;
          updated_date?: string;
        };
        Update: {
          user_id?: string;
          user_name?: string;
          email?: string;
          phone_number?: string | null;
          is_active?: boolean;
          group_names?: string[];
          zeppelin_role?: 'admin' | 'user';
          ips?: string[];
          shiro_hash?: string;
          created_date?: string;
          updated_date?: string;
        };
      };
    };
  };
}

export type UserManagement = Database['public']['Tables']['users_management']['Row'];
