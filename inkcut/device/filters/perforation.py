"""
Copyright (c) 2025, Perforation Filter Implementation.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 4, 2025

@author: Inkcut Community

Perforation Filter - Creates perforated cuts similar to Summa FlexCut
Splits continuous cutting paths into alternating cut and bridge segments
for applications like sewing pattern cutting where pieces need to stay
connected until removed.
"""
from atom.api import Float, Enum, Bool, Instance
from inkcut.device.plugin import DeviceFilter, Model
from inkcut.core.utils import unit_conversions
try:
    from enaml.qt.QtGui import QPainterPath, QPolygonF
    from enaml.qt.QtCore import QPointF
except ImportError:
    # Fallback in case of import issues
    QPainterPath = None
    QPolygonF = None
    QPointF = None


class PerforationConfig(Model):
    #: Cut length in user units (how long each cut segment should be)
    cut_length = Float(5.0, strict=False).tag(config=True)
    
    #: Bridge length in user units (how long each uncut bridge should be)
    bridge_length = Float(2.0, strict=False).tag(config=True)
    
    #: Whether to start with a cut or a bridge
    start_with_cut = Bool(True).tag(config=True)
    
    #: Units for display 
    units = Enum(*unit_conversions.keys()).tag(config=True)
    
    def _default_units(self):
        return 'mm'


class PerforationFilter(DeviceFilter):
    """Filter that creates perforated cuts by splitting paths into 
    alternating cut and bridge segments. This is useful for pattern 
    cutting where you want pieces to stay connected until removed.
    
    Similar to Summa FlexCut feature - splits continuous paths into
    segments with pen up/down commands to create perforations.
    """
    
    #: Configuration
    config = Instance(PerforationConfig, ()).tag(config=True)
    
    def apply_to_polypath(self, polypath):
        """ Apply perforation to the polypath by splitting each polygon
        into alternating cut and bridge segments.
        
        Parameters
        ----------
        polypath: List of QPolygonF
            List of polygons to process
        
        Returns
        -------
        polypath: List of QPolygonF
            List of polygons with perforation applied - will contain
            more polygons as continuous paths are split into segments
        """
        # Safety check for Qt imports
        if QPainterPath is None or QPolygonF is None:
            return polypath
            
        cut_length = self.config.cut_length
        bridge_length = self.config.bridge_length
        
        # If both lengths are 0 or negative, return unchanged
        if cut_length <= 0 and bridge_length <= 0:
            return polypath
            
        # If only cut length is set, don't perforate (continuous cut)
        if bridge_length <= 0:
            return polypath
            
        result = []
        
        try:
            for poly in polypath:
                if len(poly) < 2:
                    # Skip polygons with insufficient points
                    result.append(poly)
                    continue
                    
                # Apply perforation to this polygon
                perforated_segments = self.apply_perforation(poly, cut_length, bridge_length)
                result.extend(perforated_segments)
        except Exception:
            # If anything goes wrong, return original polypath
            return polypath
        
        return result
    
    def apply_perforation(self, poly, cut_length, bridge_length):
        """Apply perforation to a single polygon by splitting it into
        alternating cut and bridge segments.
        
        Parameters
        ----------
        poly: QPolygonF
            The polygon to perforate
        cut_length: float
            Length of each cut segment
        bridge_length: float
            Length of each bridge segment
            
        Returns
        -------
        segments: List of QPolygonF
            List of polygon segments representing the cuts
            (bridges are omitted - they become pen-up moves)
        """
        if len(poly) < 2 or QPainterPath is None:
            return [poly]
            
        try:
            # Convert polygon to QPainterPath to use length calculations
            path = QPainterPath()
            path.moveTo(poly[0])
            for i in range(1, len(poly)):
                path.lineTo(poly[i])
                
            # If path is too short to perforate meaningfully, return as-is
            total_length = path.length()
            segment_length = cut_length + bridge_length
            
            if total_length <= segment_length:
                return [poly]
                
            segments = []
            current_distance = 0.0
            is_cutting = self.config.start_with_cut
            
            while current_distance < total_length:
                if is_cutting:
                    # Create a cut segment
                    segment_start = current_distance
                    segment_end = min(current_distance + cut_length, total_length)
                    
                    if segment_end > segment_start:
                        cut_segment = self.extract_path_segment(path, segment_start, segment_end)
                        if cut_segment and len(cut_segment) >= 2:
                            segments.append(cut_segment)
                            
                    current_distance = segment_end
                else:
                    # Skip bridge segment (pen up)
                    current_distance = min(current_distance + bridge_length, total_length)
                    
                # Toggle between cutting and bridging
                is_cutting = not is_cutting
                
            return segments if segments else [poly]
        except Exception:
            # If anything goes wrong, return original polygon
            return [poly]
    
    def extract_path_segment(self, path, start_distance, end_distance):
        """Extract a segment of the path between two distance points.
        
        Parameters
        ----------
        path: QPainterPath
            The source path
        start_distance: float
            Starting distance along the path
        end_distance: float
            Ending distance along the path
            
        Returns
        -------
        segment: QPolygonF or None
            Polygon representing the path segment
        """
        if QPolygonF is None or start_distance >= end_distance:
            return None
            
        try:
            total_length = path.length()
            if start_distance >= total_length:
                return None
                
            # Convert distances to percentages
            start_percent = start_distance / total_length
            end_percent = min(end_distance / total_length, 1.0)
            
            # Get start and end points
            start_point = path.pointAtPercent(start_percent)
            end_point = path.pointAtPercent(end_percent)
            
            # For now, create a simple line segment
            # TODO: This could be enhanced to follow the exact path curve
            segment = QPolygonF()
            segment.append(start_point)
            segment.append(end_point)
            
            return segment
        except Exception:
            return None