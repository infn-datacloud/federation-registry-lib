import Provider from "./_componets/provider";
import { getProvider } from "./_lib/dataFetching";

export default async function Page({ params }: { params: { provider: string } }) {
  const provider = await getProvider(params.provider);
  return <Provider promise={provider} />;
}
