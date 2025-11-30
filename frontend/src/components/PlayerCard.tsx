interface Player {
  uid: string;
  name: string;
  onlineSince: string | null;
  lastOnline: string | null;
  isOnline: boolean;
}

interface PlayerCardProps {
  player: Player;
}

export function PlayerCard({ player }: PlayerCardProps) {
  return (
    <div className="card md:min-w-md bg-base-200 card-border">
      <div className="card-body flex flex-col gap-4">
        <div className="flex flex-row  items-center  ">
          <h2 className="card-title flex-grow w-full">{player.name}</h2>
          <p>
            {player.isOnline && (
              <span className="  badge badge-success ">Online</span>
            )}
          </p>
        </div>
        <p className="mt-4">
          {player.onlineSince
            ? `Online since ${player.onlineSince}`
            : `Last seen ${player.lastOnline}`}
        </p>
      </div>
    </div>
  );
}