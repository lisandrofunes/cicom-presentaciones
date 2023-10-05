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
      }
    })
  }

  getSelectedFiles() {
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

