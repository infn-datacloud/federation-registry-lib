"use client";

import Loading from "../loading";
import { useIdentityProviders } from "../../_lib/crud";
import Skeleton from "./_components/skeleton";

export default function Page({
  params,
}: {
  params: { identity_provider: string };
}) {
  const { identityProvider } = useIdentityProviders(params.identity_provider);
  return identityProvider ? <Skeleton item={identityProvider} /> : <Loading />;
}
