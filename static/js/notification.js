// 알림 목록 가져오기
function getNotificationList() {
  axios.get('/notifications/')
    .then(function(response) {
      // 알림 목록 데이터를 사용하여 페이지에 알림 표시
      const notificationList = document.getElementById('notification-list');
      notificationList.innerHTML = '';
      response.data.forEach(function(notification) {
        const listItem = document.createElement('li');
        listItem.textContent = notification.message;
        listItem.classList.add('notification-item');
        listItem.dataset.notificationId = notification.id;
        notificationList.appendChild(listItem);
      });
    })
    .catch(function(error) {
      // 에러 처리
      console.error(error);
    });
}

// 알림 읽음 처리
function markNotificationAsRead(notificationId) {
  axios.post(`/notifications/mark-as-read/${notificationId}/`)
    .then(function(response) {
      // 알림 읽음 처리 성공 시, 시각적으로 표시
      const notificationElement = document.getElementById(`notification-${notificationId}`);
      notificationElement.classList.add('read');
    })
    .catch(function(error) {
      // 에러 처리
      console.error(error);
    });
}

// 페이지 로드 시 알림 목록 가져오기
document.addEventListener('DOMContentLoaded', function() {
  getNotificationList();
});

// 알림 클릭 시 읽음 처리
document.addEventListener('click', function(event) {
  const target = event.target;
  if (target.classList.contains('notification-item')) {
    const notificationId = target.dataset.notificationId;
    markNotificationAsRead(notificationId);
  }
});