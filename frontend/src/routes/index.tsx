import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";

interface UserLog {
  id: number;
  uid: string;
  name: string;
  joinedAt: string;
  leftAt: string | null;
}

function formatRelativeDate(dateString: string): string {
  const [month, day, year] = dateString.split(" ")[0].split("/");
  const date = new Date(`${year}-${month}-${day} ${dateString.split(" ")[1]}`);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const inputDate = new Date(date);
  inputDate.setHours(0, 0, 0, 0);

  if (inputDate.getTime() === today.getTime()) {
    return `Today at ${date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}`;
  } else if (inputDate.getTime() === yesterday.getTime()) {
    return `Yesterday at ${date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}`;
  } else {
    const daysDiff = Math.floor(
      (today.getTime() - inputDate.getTime()) / (1000 * 60 * 60 * 24),
    );
    if (daysDiff < 7) {
      return `${daysDiff} days ago at ${date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}`;
    } else {
      return (
        date.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        }) +
        ` at ${date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}`
      );
    }
  }
}

export const Route = createFileRoute("/")({
  component: VintageLogDashboard,
});

function VintageLogDashboard() {
  const {
    data: userLogs = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["playerLogs"],
    queryFn: async () => {
      // const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`/api/players/logs`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json() as Promise<UserLog[]>;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Loading logs...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center">
            <p className="text-red-600">Error: {error.message}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Vintage Log Dashboard
          </h1>
          <p className="text-gray-600">
            User activity logs and session information
          </p>
        </div>

        <div className="grid gap-4 max-w-2xl mx-auto">
          {userLogs.map((log) => (
            <div
              key={log.id}
              className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow"
            >
              <div className="mb-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {log.name}
                  </h3>
                  {log.leftAt === null && (
                    <span className="px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full">
                      Online
                    </span>
                  )}
                </div>
                <div className="w-full h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded"></div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center text-sm">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-gray-600 font-medium">Logged On:</span>
                  <span className="ml-auto text-gray-900 text-right">
                    {formatRelativeDate(log.joinedAt)}
                  </span>
                </div>

                <div className="flex items-center text-sm">
                  <div
                    className={`w-2 h-2 rounded-full mr-2 ${log.leftAt === null ? "bg-green-500" : "bg-red-500"}`}
                  ></div>
                  <span className="text-gray-600 font-medium">
                    {log.leftAt === null ? "Status:" : "Logged Off:"}
                  </span>
                  <span className="ml-auto text-gray-900 text-right">
                    {log.leftAt === null
                      ? "Still Online"
                      : formatRelativeDate(log.leftAt)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
