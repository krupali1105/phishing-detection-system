import PhishingDetector from "@/components/PhishingDetector";
import { Suspense } from "react";
import ModernLoader from "@/components/ModernLoader";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Suspense fallback={
        <div className="flex items-center justify-center min-h-screen">
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <ModernLoader 
              text="Initializing Security System..."
              size="lg"
              variant="spinner"
            />
          </div>
        </div>
      }>
        <PhishingDetector />
      </Suspense>
    </div>
  );
}
