const forms = document.querySelectorAll('#likeform')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
forms.forEach( (likeform) => {
  likeform.addEventListener('submit', function (event) {
    event.preventDefault()
    const postId = event.target.dataset.postId
    axios({
      method: 'POST',
      url: `/${postId}/like/`,
      headers: {'X-CSRFToken':csrftoken,}
    })
    .then((response) => {
      const likeBtn = document.querySelector(`#like-${postId}`)
      const islikeusers = response.data.is_like_users
      if (islikeusers === true) {
        likeBtn.value = "하트없어"
      } else {
        likeBtn.value = "하트"
      }
    })
  })
})
