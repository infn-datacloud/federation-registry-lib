import { Suspense } from "react";
import { Provider } from "../_lib/types";
import Loading from "../loading";
import { Card, CardHeader, Grid } from "@mui/material";

export default async function ProviderGrid({
  promise,
}: {
  promise: Promise<Provider>;
}) {
  const provider = await promise;
  return (
    <Suspense fallback={<Loading />}>
      <Grid container spacing={2}>
        <Grid item>
          <Card>
            <CardHeader title="Projects" />
          </Card>
        </Grid>
      </Grid>
    </Suspense>
  );
}
