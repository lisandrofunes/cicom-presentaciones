class MediaFile {
  constructor(url, duration, index) {
    this.url = url
    this.duration = duration
    this.node = createHTMLNode({ type: fileType(url), src: url })
    this.duration = fileType(url) === 'video' ? undefined : duration
    this.type = fileType(url)
    this.index = index
  }

  setDuration(duration) {
    this.duration = duration
  }

  getFileTagChildren() {
    return this.node.children[0]
  }

  append(node) {
    node.appendChild(this.node)
  }
}

function fileType(filesUrl) {
  const imageFormats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico', 'tiff', 'tif']
  const videoFormats = ['avi', 'webm', 'mkv', 'mov', 'wmv', 'flv', '3gp', 'ogg', 'ogv', 'mpg', 'mpeg', 'm4v', 'm2v', '3g2', '3gp2', '3gpp', '3gpp2', 'mpg2', 'mp2v', 'mp2', 'mpv2', 'mpa', 'mpe', 'm1v', 'mpv', 'mp4v', 'mp4', 'm4p', 'm4b', 'm4r', 'm4v', 'f4v', 'f4p', 'f4a', 'f4b']

  const extension = filesUrl.split('.')?.pop()?.toLowerCase()

  if (imageFormats.includes(extension)) return 'image'
  if (videoFormats.includes(extension)) return 'video'
  return null
}

function createHTMLNode({ type, src }) {
  const fileType = {
    imagen: 'img',
    image: 'img',
    video: 'video',
    img: 'img',
  }[type]

  const wrapper = document.createElement('div')
  wrapper.classList.add('file-wrapper')
  wrapper.dataset.state = 'hidden'
  const node = document.createElement(fileType)
  
  if (fileType === 'img') {
    node.setAttribute('src', src)
    node.setAttribute('alt', 'Imagen')
  }

  if (fileType === 'video') {
    node.setAttribute('src', src)
    node.setAttribute('controls', true)
  }

  wrapper.appendChild(node)
  return wrapper
}

function mapFiles(rawFiles, duration) {
  const files = rawFiles.map( (url, index) => {
    return new MediaFile(url, duration, index)
})

return files
}

function videoDuration(videoTag) {
  return new Promise((resolve, reject) => {
    videoTag.onloadedmetadata = () => {
      resolve(videoTag.duration)
    }
  })
}

function nextSlide(files, file) {
  files.forEach(file => {
    file.node.dataset.state = 'hidden'
  })

  setTimeout(() => {
    file.node.dataset.state = 'visible'
    if(file.type === 'video'){
      file.getFileTagChildren().play()
        .then(() => console.log('play'))
        .catch(() => console.log('error'))
    }
  }, 500)
}

async function slide(files) {
  for (const file of files) {
    nextSlide(files, file)
    await sleep(file.duration)
    if (file.index === files.length - 1) {
      slide(files)
    }
  }
}

function sleep(time) {
  return new Promise(resolve => {
    setTimeout(() => resolve(''), time)
  })
}