const forms = document.querySelectorAll('#likeform')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value


forms.forEach((likeform) => {
  likeform.addEventListener('submit', function (event) {
    event.preventDefault()
    const postId = event.target.dataset.postId
    axios({
      method: 'POST',
      url: `/${postId}/like/`,
      headers: { 'X-CSRFToken': csrftoken }
    })
      .then((response) => {
        const likeBtn = document.querySelector(`#like-${postId}`)
        const isLikeUsers = response.data.is_like_users
        if (isLikeUsers === true) {
          likeBtn.innerHTML = '<i class="bi bi-heart-fill" style="color: red;"></i>'
        } else {
          likeBtn.innerHTML = '<i class="bi bi-heart" style="color: black;"></i>'
        }
      })
  })
})