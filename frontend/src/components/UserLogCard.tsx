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

interface UserLogCardProps {
  log: UserLog;
}

export function UserLogCard({ log }: UserLogCardProps) {
  return (
    <div className="card bg-base-200 card-border">
      <div className="card-body flex flex-col gap-4">
        <h2 className="card-title">{log.name}</h2>
        <div className="text-sm opacity-70">
          <div className="flex justify-between">
            <span>Logged On:</span>
            <span>{formatRelativeDate(log.joinedAt)}</span>
          </div>
          <div className="flex justify-between">
            <span>{log.leftAt === null ? "Status:" : "Logged Off:"}</span>
            <span>
              {log.leftAt === null
                ? "Still Online"
                : formatRelativeDate(log.leftAt)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}