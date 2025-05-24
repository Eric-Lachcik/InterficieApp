import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from 'boot/axios';

export const useNotificationsStore = defineStore('notifications', () => {
  const list = ref([]);
  const unreadCount = ref(0);

  const fetchNotifications = async (userId) => {
    try {
      const response = await api.get('/api/notifications/', {
        headers: { 'X-User-ID': userId }
      });
      list.value = response.data;
      unreadCount.value = list.value.filter(n => !n.read).length;
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  return { list, unreadCount, fetchNotifications };
});