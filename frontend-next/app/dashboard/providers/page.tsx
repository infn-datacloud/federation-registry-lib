import { getProviders } from "../_lib/crud";
import ProviderGrid from "./_components/providers";

export default async function Page() {
  const providers = await getProviders();
  return <ProviderGrid promise={providers} />;
}
