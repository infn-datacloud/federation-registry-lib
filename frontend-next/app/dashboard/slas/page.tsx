import { Grid } from "@mui/material";
import { Suspense } from "react";
import SLACardContent from "./_components/slaCardContent";
import Loading from "../slas/loading";
import { getSLAs } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { SLA } from "./_lib/dbTypes";

export default async function Page() {
  const slas: SLA[] = await getSLAs();
  let children = slas.map((sla, index) => (
    <Grid item key={index}>
      <CardWrapper kind="slas" name="SLA" uid={sla.uid}>
        <SLACardContent item={sla} />
      </CardWrapper>
    </Grid>
  ));
  return (
    <Suspense fallback={<Loading />}>
      <Grid container spacing={2}>
        {children}
      </Grid>
    </Suspense>
  );
}
