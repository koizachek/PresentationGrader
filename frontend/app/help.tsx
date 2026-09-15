"use client";

import { useEffect, useRef, useState } from "react";

export function Help({ text, label = "Hilfe" }: { text: string; label?: string }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent | KeyboardEvent) => {
      if (e instanceof KeyboardEvent && e.key !== "Escape") return;
      if (e instanceof MouseEvent && ref.current?.contains(e.target as Node)) return;
      setOpen(false);
    };
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", close);
    return () => { document.removeEventListener("mousedown", close); document.removeEventListener("keydown", close); };
  }, [open]);

  return (
    <span className="help" ref={ref}>
      <button type="button" aria-label={label} aria-expanded={open} onClick={(e) => { e.preventDefault(); e.stopPropagation(); setOpen((o) => !o); }}>?</button>
      {open && <span className="pop" role="tooltip">{text}</span>}
    </span>
  );
}
