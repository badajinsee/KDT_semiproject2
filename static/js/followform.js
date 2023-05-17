const forms = document.querySelectorAll('[id^="follow_form"]')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
forms.forEach((follow_form) => {
  follow_form.addEventListener('submit', function (event) {
    event.preventDefault()
    const followBtn = event.currentTarget.querySelector('input[type="submit"]');
    const userId = event.target.dataset.userId
    axios({
      method: 'POST',
      url: `/accounts/${userId}/follow/`,
      headers: { 'X-CSRFToken': csrftoken }
    })
    .then((response) => {
      const isFollowed = response.data.is_followed
      if (isFollowed === true) {
        followBtn.value = '팔로잉'
      } else {
        followBtn.value = '팔로우'
      }
      console.log(isFollowed, followBtn)
      })
  })
})