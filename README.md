# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

---

## Development & Electron

This repository contains a React/Vite frontend located under the `Frontend/` folder and an Electron wrapper in `Electron/`.

### Running the web UI

1. Install dependencies (including Electron):
   ```bash
   npm install
   # or, if you only need Electron for development:
   npm install --save-dev electron
   ```
2. Start the Vite dev server. By default it listens on port `5173` and will fail if
   the port is already in use (see `vite.config.js`):
   ```bash
   npm run dev
   ```
3. Open the URL printed in the console (e.g. `http://localhost:5173`).

### Running in Electron

1. Make sure the dev server is running (step above) or build the app:
   ```bash
   npm run build
   ```
2. Run Electron from the project root:
   ```bash
   npm run electron
   ```
   You can also start the server and Electron side-by-side by opening two
   terminals – one with `npm run dev` and one with `npm run electron`.

Electron’s `main.js` uses the `PORT` environment variable when available,
falling back to `5173`. The window will load the dev server in development mode
and the local `index.html` file when the app has been packaged.
