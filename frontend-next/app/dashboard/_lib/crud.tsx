import path from "path";
import useSWR from "swr";

const baseUrl = "http://localhost:8000/";

async function get(basePath: string, uid?: string) {
  let suffix = basePath;
  if (uid !== undefined) {
    suffix = path.join(basePath, uid);
  }
  let targetUrl = new URL(suffix, baseUrl);

  const res = await fetch(targetUrl.toString());
  if (res.status != 200) {
    throw new Error("Failed to fetch data");
  }
  return res.json();
}

export function useFlavors(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["flavors/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { flavor: data, error, isLoading, isValidating };
  else return { flavors: data, error, isLoading, isValidating };
}

export function useIdentityProviders(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["identity_providers/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { identityProvider: data, error, isLoading, isValidating };
  return { identityProviders: data, error, isLoading, isValidating };
}

export function useImages(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["images/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { image: data, error, isLoading, isValidating };
  return { images: data, error, isLoading, isValidating };
}

export function useLocations(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["locations/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { location: data, error, isLoading, isValidating };
  return { locations: data, error, isLoading, isValidating };
}

export function useProjects(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["projects/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { project: data, error, isLoading, isValidating };
  return { projects: data, error, isLoading, isValidating };
}

export function useProviders(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["providers/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { provider: data, error, isLoading, isValidating };
  return { providers: data, error, isLoading, isValidating };
}

export function useServices(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["services/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { service: data, error, isLoading, isValidating };
  return { services: data, error, isLoading, isValidating };
}

export function useSLAs(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["slas/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { sla: data, error, isLoading, isValidating };
  return { slas: data, error, isLoading, isValidating };
}

export function useUserGroup(uid?: string) {
  const { data, error, isLoading, isValidating } = useSWR(
    ["user_groups/", uid],
    async ([basePath, uid]) => await get(basePath, uid)
  );
  if (uid) return { userGroup: data, error, isLoading, isValidating };
  return { userGroups: data, error, isLoading, isValidating };
}
