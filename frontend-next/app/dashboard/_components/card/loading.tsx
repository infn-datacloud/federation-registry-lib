import { Card, CardContent, CardHeader, Skeleton } from "@mui/material";
import { Fragment } from "react";
import { cardMaxWidth, cardMediaHeight } from "../../_lib/constants";

const skeletonCardMediaHeight = cardMediaHeight + 60;
const skeletonCardTextHeight = 10;
const skeletonCardTextMarginBottom = 6;

export default function LoadingCard() {
  return (
    <Card sx={{ maxWidth: cardMaxWidth }}>
      <CardHeader
        title={
          <Skeleton
            animation="wave"
            height={skeletonCardTextHeight}
            style={{ marginBottom: skeletonCardTextMarginBottom }}
          />
        }
        subheader={
          <Skeleton
            animation="wave"
            height={skeletonCardTextHeight}
            width="40%"
            style={{ marginBottom: skeletonCardTextMarginBottom }}
          />
        }
      />
      <Skeleton
        sx={{ height: skeletonCardMediaHeight }}
        animation="wave"
        variant="rectangular"
      />
      <CardContent>
        <Fragment>
          <Skeleton
            animation="wave"
            height={skeletonCardTextHeight}
            style={{ marginBottom: skeletonCardTextMarginBottom }}
          />
          <Skeleton
            animation="wave"
            height={skeletonCardTextHeight}
            style={{ marginBottom: skeletonCardTextMarginBottom }}
          />
          <Skeleton
            animation="wave"
            height={skeletonCardTextHeight}
            style={{ marginBottom: skeletonCardTextMarginBottom }}
          />
        </Fragment>
      </CardContent>
    </Card>
  );
}
