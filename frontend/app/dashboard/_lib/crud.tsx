import path from "path";
import useSWR from "swr";

async function get(basePath: string, apiVersion: string, uid?: string) {
  const apiUrl = `http://${process.env.NEXT_PUBLIC_DOMAIN}`;

  let suffix = path.join("api", apiVersion, basePath, "/");
  if (uid !== undefined) {
    suffix = path.join(suffix, uid);
  }
  let targetUrl = new URL(suffix, apiUrl);

  const res = await fetch(targetUrl.toString());
  if (res.status != 200) {
    throw new Error("Failed to fetch data");
  }
  return res.json();
}

export function useFlavors(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["flavors", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { flavor: data, error, isLoading, isValidating };
  else return { flavors: data, error, isLoading, isValidating };
}

export function useIdentityProviders(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["identity_providers", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { identityProvider: data, error, isLoading, isValidating };
  return { identityProviders: data, error, isLoading, isValidating };
}

export function useImages(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["images", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { image: data, error, isLoading, isValidating };
  return { images: data, error, isLoading, isValidating };
}

export function useLocations(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["locations", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { location: data, error, isLoading, isValidating };
  return { locations: data, error, isLoading, isValidating };
}

export function useProjects(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["projects", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { project: data, error, isLoading, isValidating };
  return { projects: data, error, isLoading, isValidating };
}

export function useProviders(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["providers", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { provider: data, error, isLoading, isValidating };
  return { providers: data, error, isLoading, isValidating };
}

export function useServices(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["services", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { service: data, error, isLoading, isValidating };
  return { services: data, error, isLoading, isValidating };
}

export function useSLAs(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["slas", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { sla: data, error, isLoading, isValidating };
  return { slas: data, error, isLoading, isValidating };
}

export function useUserGroup(uid?: string, apiVersion: string = "v1") {
  const { data, error, isLoading, isValidating } = useSWR(
    ["user_groups", apiVersion, uid],
    async ([basePath, apiVersion, uid]) => await get(basePath, apiVersion, uid)
  );
  if (uid) return { userGroup: data, error, isLoading, isValidating };
  return { userGroups: data, error, isLoading, isValidating };
}
