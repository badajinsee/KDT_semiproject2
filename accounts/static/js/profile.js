const forms = document.querySelector('#follow-form')
const form2 = document.querySelectorAll('#followform2')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  forms.addEventListener('submit', function (event) {
    event.preventDefault()
    const userId = event.target.dataset.userId
      axios({
        method: 'post',
        url: `/accounts/${userId}/follow/`,
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then((response) => {
        const isFollowed = response.data.is_followed
        const followBtn = document.querySelector('#follow-form > input[type=submit]')
        if (isFollowed === true) {
          followBtn.value = '언팔로우'
        } else {
          followBtn.value = '팔로우'
        }
        const followingsCountTag = document.querySelector('#followings-count')
        const followersCountTag = document.querySelector('#followers-count')
        const followingsCountData = response.data.followings_count
        const followersCountData = response.data.followers_count
        followingsCountTag.textContent = followingsCountData
        followersCountTag.textContent = followersCountData
      })
  })
  form2.forEach( (followform2) => {
    followform2.addEventListener('submit', function (event) {
      event.preventDefault()
      const userId = event.target.dataset.userId
      axios({
        method: 'POST',
        url: `/accounts/${userId}/follow/`,
        headers: {'X-CSRFToken':csrftoken,}
      })
      .then((response) => {
        const isFollowed = response.data.is_followed
        const followBtn = document.querySelector(`#followform2 > input[type=submit]`)
        console.log(followBtn,isFollowed )
  
        if (isFollowed === true) {
          followBtn.value = "언팔로우"
        } else {
          followBtn.value = "팔로우"
        }
      })
    })
  })