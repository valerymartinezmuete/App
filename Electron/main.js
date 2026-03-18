const { app, BrowserWindow } = require("electron")
const path = require("path")
const { spawn } = require("child_process")

let backendProcess

function startBackend() {

  const backendPath = path.join(__dirname, "../Backend/dist/app.exe")

  backendProcess = spawn(backendPath)

}

function createWindow() {

  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    icon: path.join(__dirname, "../assets/icon.ico")
  })

  win.loadFile(path.join(__dirname, "../dist/index.html"))

}

app.whenReady().then(async () => {

  startBackend()

    setTimeout(() => {
      createWindow()
    }, 3000)

  createWindow()

})

app.on("window-all-closed", () => {

  if (backendProcess) backendProcess.kill()

  if (process.platform !== "darwin") {
    app.quit()
  }

})