/* Copyright (c) Dario Pizzolante */
import { useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";

const VISIBILITY_OFFSET = 280;

export function ScrollToTopButton() {
  const [isVisible, setIsVisible] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }

    return window.scrollY > VISIBILITY_OFFSET;
  });

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const handleScroll = () => {
      setIsVisible(window.scrollY > VISIBILITY_OFFSET);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  function handleScrollToTop() {
    if (typeof window === "undefined") {
      return;
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <button
      aria-hidden={!isVisible}
      aria-label="Scroll to top"
      className={`scroll-to-top ${isVisible ? "scroll-to-top--visible" : ""}`}
      tabIndex={isVisible ? 0 : -1}
      type="button"
      onClick={handleScrollToTop}
    >
      <ArrowUp className="size-5" />
    </button>
  );
}
