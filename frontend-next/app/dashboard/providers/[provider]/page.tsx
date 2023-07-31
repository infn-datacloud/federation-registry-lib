import { Suspense } from "react";
import Loading from "../loading";
import { getProviders } from "../../_lib/crud";
import Skeleton from "./_components/skeleton";

export default async function Page({
  params,
}: {
  params: { provider: string };
}) {
  const provider = await getProviders(params.provider);
  return (
    <Suspense fallback={<Loading />}>
      <Skeleton item={provider} />
    </Suspense>
  );
}
