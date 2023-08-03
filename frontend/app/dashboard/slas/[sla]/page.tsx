"use client";

import Loading from "../loading";
import { useSLAs } from "../../_lib/crud";
import Skeleton from "./_components/skeleton";

export default function Page({ params }: { params: { provider: string } }) {
  const { sla } = useSLAs(params.provider);
  return sla ? <Skeleton item={sla} /> : <Loading />;
}
