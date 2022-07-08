
##################################################
##################################################
##################################################

#' Run PCA
#'
#' Run PCA on matrix
#' @param df data frame of normalised counts
#' @export
#' @examples
#' runPCA(df)

runPCA <- function(df, scale=TRUE){

    pc <- prcomp(t(df), scale=scale)
    return (pc)
}

##################################################
##################################################
##################################################

#' Get PCA
#'
#' Get princple components
#' @param pc prcomp object
#' @export
#' @examples
#' getPCA(runPCA(df))

getPCA <- function(pc){

    pcs <- data.frame(pc$x)
    return(pcs)
}

##################################################
##################################################
##################################################

#' Get variance explained
#'
#' Get variance explained for prcomp object
#' @param pc prcomp object
#' @param component string (component to get VE for)
#' @export
#' @examples
#' getVE(runPCA(df))

getVE <- function(pc, component="PC1"){

    pve <- base::summary(pc)$importance[,component][[2]]
    return (pve)
}


##################################################
##################################################
##################################################

#' Plot PCA
#'
#' Plot PCA of dataset of interest
#' @param pc prcomp object
#' @param colourby vector of conditions
#' @param pcs vector of pcs to plot
#' @export
#' @examples
#' plotPCA(PCA(mat))

plotPrincipleComponents <- function(pc, metadata, colourby="none", shapeby="none", group="none", continuous=FALSE,  pcs=c("PC1", "PC2")){

    # covariate must be in same order as pc rownames

    # get variance explained for each component
    ve1 <- getVE(pc, component=pcs[1])
    ve2 <- getVE(pc, component=pcs[2])

    ve1 <- round(ve1, 2)*100
    ve2 <- round(ve2, 2)*100

    # get data frame of components
    pca <- data.frame(pc$x)

    # add conditions
    if (colourby == "none"){
        pca$condition <- "none"}else{
    pca$condition <- metadata[,colourby]}

    # add shape
    if (shapeby == "none"){
        pca$shape <- "none"}else{
    pca$shape <- metadata[,shapeby]}#

    if (group == "none"){
        pca$group <- "none"}else{
    pca$group <- metadata[,group]}

    if (continuous==FALSE){
       pca$condition <- factor(pca$condition, levels=unique(pca$condition))
    }

    # plot
    pc1 <- pcs[1]
    pc2 <- pcs[2]

    # labels
    xlabel <- paste(pc1, ve1, sep=" (")
    xlabel <- paste(xlabel, "%", sep="")
    xlabel <- paste(xlabel, ")", sep="")
    ylabel <- paste(pc2, ve2, sep=" (")
    ylabel <- paste(ylabel, "%", sep="")	
    ylabel <- paste(ylabel, ")", sep="")

    n <- length(unique(pca$condition))
    colours <- rainbow(n, s=0.7, v=0.6)
    
    plot1 <- ggplot(pca, aes_string(x=pc1, y=pc2, group="group", colour="condition", shape="shape"))
    plot2 <- plot1 + geom_point(size=3)
    plot3 <- plot2 + theme_bw() 
    plot4 <- plot3 + xlab(xlabel) + ylab(ylabel)
    if (continuous==TRUE){
        plot4 <- plot4 + scale_colour_gradient()}
    else{
        plot4 <- plot4 + scale_colour_manual(values=colours)
	}
    return(plot4) 
}
