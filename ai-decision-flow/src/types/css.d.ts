// src/types/css.d.ts

// Global declaration for standard CSS imports (e.g. import './globals.css')
declare module "*.css" {
  const content: { [className: string]: string };
  export default content;
}

// Declaration for xyflow library CSS
declare module "@xyflow/react/dist/style.css" {
  const content: { [className: string]: string };
  export default content;
}