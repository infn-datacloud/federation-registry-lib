import { Suspense } from "react";
import Loading from "../loading";
import { getProviders } from "../../_lib/crud";
import ProviderSkeleton from "./_componets/providerSkeleton";

export default async function Page({
  params,
}: {
  params: { provider: string };
}) {
  const provider = await getProviders(params.provider);
  return (
    <Suspense fallback={<Loading />}>
      <ProviderSkeleton provider={provider} />
    </Suspense>
  );
}
