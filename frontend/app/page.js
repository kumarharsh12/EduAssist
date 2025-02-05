import Image from "next/image";
import Link from "next/link";
import { ThreeDCardDemo } from "./components/card";

export default function Home() {
  return (
    <>
      <div className="bg-gradient-to-r from-zinc-800 to-red-950">
        <ThreeDCardDemo />
      </div>
    </>
  );
}
