"use client";

import Loading from "../loading";
import { useProviders } from "../../_lib/crud";
import Skeleton from "./_components/skeleton";

export default function Page({ params }: { params: { provider: string } }) {
  const { provider } = useProviders(params.provider);
  return provider ? <Skeleton item={provider} /> : <Loading />;
}
