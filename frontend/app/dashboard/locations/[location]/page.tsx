"use client";

import Loading from "../loading";
import { useLocations } from "../../_lib/crud";
import Skeleton from "./_components/skeleton";

export default function Page({ params }: { params: { location: string } }) {
  const { location } = useLocations(params.location);
  return location ? <Skeleton item={location} /> : <Loading />;
}
