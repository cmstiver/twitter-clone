export function getRelativeTime(timestamp: string): string {
  console.log(timestamp);
  const now = new Date();
  const created = new Date(timestamp);

  const elapsedMs = now.getTime() - created.getTime();

  const MINUTE_MS = 60 * 1000;
  const HOUR_MS = 60 * MINUTE_MS;
  const DAY_MS = 24 * HOUR_MS;

  if (elapsedMs < MINUTE_MS) {
    return "Just now";
  } else if (elapsedMs < HOUR_MS) {
    const minutes = Math.floor(elapsedMs / MINUTE_MS);
    return `${minutes}m`;
  } else if (elapsedMs < DAY_MS) {
    const hours = Math.floor(elapsedMs / HOUR_MS);
    return `${hours}h`;
  } else {
    const month = created.toLocaleString("default", { month: "long" });
    const day = created.getDate();
    const year = created.getFullYear();
    if (year === now.getFullYear()) {
      return `${month} ${day}`;
    } else {
      return `${month} ${day}, ${year}`;
    }
  }
}

export function formatDate(dateString: string) {
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  const date = new Date(dateString);

  const hour = date.getHours();
  const minute = date.getMinutes();
  const amPm = hour >= 12 ? "PM" : "AM";
  const formattedHour = hour % 12 === 0 ? 12 : hour % 12;
  const formattedMinute = minute.toString().padStart(2, "0");

  const day = date.getDate();
  const month = months[date.getMonth()];
  const year = date.getFullYear();

  return `${formattedHour}:${formattedMinute} ${amPm} · ${month} ${day}, ${year}`;
}
