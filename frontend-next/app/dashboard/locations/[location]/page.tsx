import { Suspense } from "react";
import Loading from "../loading";
import { getLocations } from "../../_lib/crud";
import Skeleton from "./_componets/skeleton";

export default async function Page({
  params,
}: {
  params: { location: string };
}) {
  const location = await getLocations(params.location);
  return (
    <Suspense fallback={<Loading />}>
      <Skeleton item={location} />
    </Suspense>
  );
}
