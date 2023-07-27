import path from "path";

const baseUrl = "http://localhost:8000/";

async function get(basePath: string, uid?: string) {
  let suffix = basePath;
  if (uid !== undefined) {
    suffix = path.join(basePath, uid);
  }
  let targetUrl = new URL(suffix, baseUrl);

  const res = await fetch(targetUrl, {
    cache: "no-store",
  });
  if (res.status != 200) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}

export async function getFlavors(uid?: string) {
  return await get("flavors/", uid);
}

export async function getIdentityProviders(uid?: string) {
  return await get("identity_providers/", uid);
}

export async function getImages(uid?: string) {
  return await get("images/", uid);
}

export async function getLocations(uid?: string) {
  return await get("locations/", uid);
}

export async function getProjects(uid?: string) {
  return await get("projects/", uid);
}

export async function getProviders(uid?: string) {
  return await get("providers/", uid);
}

export async function getServices(uid?: string) {
  return await get("services/", uid);
}

export async function getSLAs(uid?: string) {
  return await get("slas/", uid);
}

export async function getUserGroup(uid?: string) {
  return await get("user_groups/", uid);
}
