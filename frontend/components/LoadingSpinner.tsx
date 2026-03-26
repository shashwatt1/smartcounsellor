export default function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-16">
      <div className="relative w-16 h-16">
        <div className="absolute top-0 w-full h-full border-4 border-slate-200 rounded-full"></div>
        <div className="absolute top-0 w-full h-full border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
      </div>
    </div>
  );
}
