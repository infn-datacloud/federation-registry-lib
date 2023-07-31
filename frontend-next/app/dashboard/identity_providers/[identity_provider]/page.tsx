import { Suspense } from "react";
import Loading from "../loading";
import { getIdentityProviders } from "../../_lib/crud";
import Skeleton from "./_componets/skeleton";

export default async function Page({
  params,
}: {
  params: { identity_provider: string };
}) {
  const identity_provider = await getIdentityProviders(params.identity_provider);
  return (
    <Suspense fallback={<Loading />}>
      <Skeleton item={identity_provider} />
    </Suspense>
  );
}
