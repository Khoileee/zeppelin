export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePhoneNumber = (phone: string): boolean => {
  const phoneRegex = /^(0|\+84)[0-9]{9,10}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};

export const validateIPv4 = (ip: string): boolean => {
  const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipRegex.test(ip.trim());
};

export const validateIPList = (ipString: string): { valid: boolean; invalidIPs: string[] } => {
  const ips = ipString.split('\n').map(ip => ip.trim()).filter(ip => ip.length > 0);
  const invalidIPs: string[] = [];

  ips.forEach(ip => {
    if (!validateIPv4(ip)) {
      invalidIPs.push(ip);
    }
  });

  return {
    valid: invalidIPs.length === 0,
    invalidIPs
  };
};

export const generateUserName = (): string => {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 5);
  return `usr_${timestamp}${random}`;
};

// Tạo Shiro hash từ password (SHA-256 base64)
export const generateShiroHash = async (password: string): Promise<string> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const base64Hash = btoa(String.fromCharCode(...hashArray));
  return `$shiro1$SHA-256$500000$${base64Hash}`;
};
