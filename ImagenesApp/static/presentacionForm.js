const defaultOptionNode = document.createElement('option')
defaultOptionNode.value = ''
defaultOptionNode.innerText = 'Seleccione una opción'

class FilesController {
  filesList = []
  selectedFiles = []
  constructor(files, galleryNode) {
    this.galleryNode = galleryNode
    this.filesList = files
  }

  render() {
    console.log('enter render')
    this.galleryNode.innerHTML = ''

    this.filesList.forEach(file => {
      const selected = this.selectedFiles.some(f => f.id === file.id)
      const fileCardDiv = document.createElement('div')
      fileCardDiv.classList.add('file-card')
      fileCardDiv.dataset.id = file.id
      fileCardDiv.dataset.selected = selected

      fileCardDiv.innerHTML = `
        ${file.video
          ? ` <video src="${file.url}" class="file-image" controls="false" autoplay="false"
        controlslist="nodownload noplaybackrate"></video>`
          : `<img src="${file.url}" alt="" class="file-image">`
        }
        <footer class="card-footer_">
          <h3>${file.nombre}</h3>
          <p>ID ${file.id}</p>
        </footer>
      `
      fileCardDiv.addEventListener('click', () => {
        this.toggleCard(fileCardDiv, file.id)
      })

      return this.galleryNode.appendChild(fileCardDiv)
    })
  }

  toggleCard(cardNode, fileID) {
    const selected = cardNode.dataset.selected === 'true'
    cardNode.dataset.selected = !selected

    if (!selected) {
      cardNode.dataset.id = fileID
      const file = this.filesList.find(f => f.id === fileID)
      this.selectedFiles.push(file)
    } else {
      const index = this.selectedFiles.findIndex(f => f.id === fileID)
      this.selectedFiles.splice(index, 1)
      cardNode.dataset.index = ''
    }
    this.updateCards()
  }

  updateCards() {
    this.galleryNode.querySelectorAll('.file-card').forEach(cardNode => {
      if (cardNode.dataset.selected === 'true') {
        const fileID = cardNode.dataset.id
        const file = this.filesList.find(f => f.id === fileID)
        if (file) {
          cardNode.dataset.selected = true
          cardNode.dataset.index = this.selectedFiles.findIndex(f => f.id === fileID) + 1
        }
        if (!this.selectedFiles.some(f => f.id === fileID)) {
          cardNode.dataset.selected = false
        }
      }
    })
  }

  getSelectedFiles() {
    return this.selectedFiles
  }

  removeSelectedFile(fileID) {
    const newSelectedFiles = this.selectedFiles.filter(f => f.id !== fileID)
    this.selectedFiles = newSelectedFiles
    return this.selectedFiles
  }
}

function getArchivosFromString(djangoString) {
  const archivosString = djangoString.replace(/( |\n)/g, "").replace('},}', '}}')
  const archivos = JSON.parse(archivosString)

  Object.values(archivos).forEach(archivo => {
    archivo.video = archivo.video === 'True'
  })

  return Object.values(archivos)
}

function renderSelectedFiles(fileController, fileBox) {
  const selectedFiles = fileController.getSelectedFiles()
  fileBox.innerHTML = ''

  selectedFiles.forEach((file, index) => {
    const selectedFileCard = document.createElement('li')
    selectedFileCard.classList.add('selectedFile')
    selectedFileCard.dataset.id = file.id
    selectedFileCard.dataset.orden = index + 1
    selectedFileCard.name = 'archivos[]'
    selectedFileCard.value = file.id
    const media = file.video ?
      `<video src="${file.url}" controls="false" autoplay="false"
        controlslist="nodownload noplaybackrate"></video>`
      : `<img src="${file.url}" alt="" `

    const innerHTML = `
      <input type="hidden" name="archivos[]" value="${file.id}">
      <div class="selectedFile-body">
        <div class="selectedFile-titleWrapper">
          <span class="selectedFile-index">${index + 1}.</span>
          <h3 class="selectedFile-title" title="${file.nombre}">${file.nombre}</h3>
        </div>
        ${media}
      </div>
    `
    selectedFileCard.innerHTML = innerHTML

    const button = document.createElement('button')
    button.classList.add('selectedFile-delete')
    button.innerText = '✖︎'
    button.type = 'button'

    button.addEventListener('click', () => {
      const fileID = selectedFileCard.dataset.id
      fileController.removeSelectedFile(fileID)
      renderSelectedFiles(fileController, fileBox)
    })
    selectedFileCard.appendChild(button)

    fileBox.appendChild(selectedFileCard)
  })
}