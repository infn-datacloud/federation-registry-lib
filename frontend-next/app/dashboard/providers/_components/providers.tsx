import { Grid } from "@mui/material";
import { Suspense } from "react";
import ProviderCard from "./provider";
import { Provider } from "../../_lib/types";
import Loading from "../loading";

export default async function ProviderGrid({
  promise,
}: {
  promise: Promise<Provider[]>;
}) {
  const providers = await promise;
  return (
    <Suspense fallback={<Loading />}>
      <Grid container spacing={2}>
        {providers.map((provider, index) => (
          <Grid item key={index}>
            <ProviderCard item={provider} />
          </Grid>
        ))}
      </Grid>
    </Suspense>
  );
}
