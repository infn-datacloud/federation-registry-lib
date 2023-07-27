export async function getProviders() {
  const res = await fetch("http://localhost:8000/providers/", {
    cache: "no-store",
  });
  if (res.status != 200) {
    throw new Error("Failed to fetch data");
  }
  return res.json();
}
