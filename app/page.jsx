"use client";

import { useState } from "react";

export default function Home() {
  const [selectedFileName, setSelectedFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = event => {
    const fileInput = event.target;
    if (fileInput.files.length > 0) {
      setSelectedFileName(fileInput.files[0]);
    }
  };

  const submitTranscription = async () => {
    if (!selectedFileName) {
      setError("Please select a file");
      return;
    }

    try {
      setLoading(true);
      setTranscript("");
      setError("");

      const formData = new FormData();
      formData.append("file", selectedFileName);

      const response = await fetch("http://localhost:3000/api/transcribe", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setTranscript(result.transcript);
    } catch (err) {
      console.log("Error on client", err);
      setError("An error occurred during transcription.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col px-24 bg-gray-50 dark:bg-gray-800 h-screen">
      <form
        className="self-center grid place-items-center w-[80%] h-full"
        onSubmit={e => {
          e.preventDefault();
          submitTranscription();
        }}>
        <div className="w-[95%] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
          <div className="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
            <textarea
              id="resultArea"
              rows={25}
              className="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"
              disabled
              value={transcript || error}></textarea>
          </div>
          <div className="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
            <div className="flex ps-0 space-x-1 rtl:space-x-reverse sm:ps-2">
              <label
                htmlFor="audioFile"
                className="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                <svg
                  className="w-4 h-4"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 12 20">
                  <path
                    stroke="currentColor"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M1 6v8a5 5 0 1 0 10 0V4.5a3.5 3.5 0 1 0-7 0V13a2 2 0 0 0 4 0V6"
                  />
                </svg>
                <input
                  type="file"
                  id="audioFile"
                  className="hidden"
                  accept=".mp3"
                  onChange={handleFileChange}
                />
              </label>
              {selectedFileName && (
                <span className="text-gray-500 mt-1">
                  {selectedFileName.name}
                </span>
              )}
            </div>

            {!loading && (
              <button
                type="submit"
                className="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800">
                Transcribe
              </button>
            )}

            {loading && (
              <div className="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center">
                <svg
                  aria-hidden="true"
                  className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-red-600"
                  viewBox="0 0 100 101"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor"
                  />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill"
                  />
                </svg>
                <span className="sr-only">Loading...</span>
              </div>
            )}
          </div>
        </div>
      </form>
    </main>
  );
}
