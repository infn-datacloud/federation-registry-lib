import { getProviders } from "../../_lib/crud";
import Provider from "./_componets/provider";

export default async function Page({
  params,
}: {
  params: { provider: string };
}) {
  const provider = await getProviders(params.provider);
  return <Provider promise={provider} />;
}
