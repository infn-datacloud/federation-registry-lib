import ProviderGrid from "./_components/providers";
import { getProviders } from "./_lib/dataFetching";

export default async function Page() {
  const providers = await getProviders();
  return <ProviderGrid promise={providers} />;
}
