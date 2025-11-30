import { createFileRoute } from "@tanstack/react-router";
import { UserLogCard } from "@/components/UserLogCard";
import { PlayerCard } from "@/components/PlayerCard";
import { useQuery } from "@tanstack/react-query";

interface UserLog {
  id: number;
  uid: string;
  name: string;
  joinedAt: string;
  leftAt: string | null;
}

export const Route = createFileRoute("/")({
  component: VintageLogDashboard,
});

type Player = {
  uid: string;
  name: string;
  onlineSince: string | null;
  lastOnline: string | null;
  isOnline: boolean;
};

function VintageLogDashboard() {
  const {
    isLoading,
    error,
    data: userLogs = [],
  } = useQuery({
    queryKey: ["playerLogs"],
    queryFn: async () => {
      const apiUrl = import.meta.env.VITE_API_URL || "/api";
      const response = await fetch(apiUrl + "/players/logs");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json() as Promise<UserLog[]>;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const {
    isLoading: isLoadingPlayers,
    error: errorPlayers,
    data: playerss = [],
  } = useQuery({
    queryKey: ["players"],
    queryFn: async () => {
      const apiUrl = import.meta.env.VITE_API_URL || "/api";
      const response = await fetch(apiUrl + "/players");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json() as Promise<Player[]>;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  console.log(playerss);
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

  const players: Player[] = [
    {
      uid: "player-1",
      name: "Simon",
      onlineSince: "2025-01-15T10:30:00Z",
      lastOnline: null,
      isOnline: true,
    },
    {
      uid: "player-2",
      name: "John",
      onlineSince: null,
      lastOnline: "2025-01-14T22:15:00Z",
      isOnline: false,
    },
    {
      uid: "player-3",
      name: "Jane",
      onlineSince: "2025-01-15T09:45:00Z",
      lastOnline: null,
      isOnline: true,
    },
    {
      uid: "player-4",
      name: "Bob",
      onlineSince: null,
      lastOnline: "2025-01-13T18:30:00Z",
      isOnline: false,
    },
  ];

  return (
    <div className="h-screen flex  flex-col gap-4 bg-base-100 lg:px-10 px-4 pt-12 pb-4">
      <h1 className="text-4xl font-sans mb-6">Vintage Log Dashboard</h1>
      <div className=" flex flex-1 w-full gap-3 flex-row min-h-0 ">
        <div className="md:flex hidden flex-col gap-3  w-full">
          <div className="text-xl mb-3">Player Logs</div>
          <div className="flex flex-col overflow-auto flex-1 gap-3 min-h-0">
            {userLogs.map((log) => (
              <UserLogCard key={log.id} log={log} />
            ))}
          </div>
        </div>
        <div className=" flex flex-1 w-full flex-col gap-3  ">
          <div className="text-xl ">Online Players</div>
          <div className="h-[1.3px] w-full bg-gray-500" />
          {players
            .filter((player) => player.isOnline)
            .map((player) => (
              <PlayerCard key={player.uid} player={player} />
            ))}

          <div className="text-xl">Offline Players</div>
          <div className="h-[1.3px] w-full bg-gray-500" />
          {players
            .filter((player) => !player.isOnline)
            .map((player) => (
              <PlayerCard key={player.uid} player={player} />
            ))}
        </div>
      </div>
    </div>
  );
}
