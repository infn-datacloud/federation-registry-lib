import { rowsPerPageOptions } from "@/app/dashboard/_lib/constants";
import {
  Box,
  Paper,
  TableContainer,
  TablePagination,
  Typography,
} from "@mui/material";
import { ChangeEvent, ReactNode, useState } from "react";

export default function PaginatedTable({
  title,
  items,
  renderItem,
}: {
  title: string;
  items: any[];
  renderItem: (items: any[], page: number, rowsPerPage: number) => ReactNode;
}) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Box>
      <Typography variant="h6">{title}</Typography>
      {items.length > 0 ? (
        <Paper>
          <TableContainer>
            {renderItem(items, page, rowsPerPage)}
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={rowsPerPageOptions}
            component="div"
            count={items.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      ) : (
        "No " + title
      )}
    </Box>
  );
}
